from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Min
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from suziai_human_annotation.core.forms import AnnotationForm
from suziai_human_annotation.core.models import Annotation, Sample
from suziai_human_annotation.core.models.choices import PitchChoices, SecondaryChoices


class DefaultView(LoginRequiredMixin, TemplateView):
    template_name = "suziai_human_annotation/core/error_no_samples.html"

    def get(self, request, *args, **kwargs):
        num_samples = Sample.objects.filter(group=self.request.user.id % 2).count()

        if not num_samples:
            return super().get(request, *args, **kwargs)

        first_sample_without_annotation_id = Sample.objects.exclude(
            annotations__in=Annotation.objects.filter(user=self.request.user),
        ).aggregate(first=Min("id"))["first"]

        if first_sample_without_annotation_id is None:
            first_sample_without_annotation_id = Sample.objects.aggregate(first=Min("id"))["first"]

        return redirect("annotate", sample_id=first_sample_without_annotation_id)


class AnnotateView(LoginRequiredMixin, TemplateView):
    template_name = "suziai_human_annotation/core/annotate.html"

    def get_context_data(self, sample_id: int = None, **kwargs):
        context = super().get_context_data(**kwargs)

        samples = Sample.objects.filter(group=self.request.user.id % 2)
        annotations = Annotation.objects.filter(user=self.request.user, sample__in=samples)
        num_samples = samples.count()
        navigation = {s.id: s.get_annotation_state(annotations) for s in samples}
        num_previous_samples = samples.filter(id__lt=sample_id).count()
        sample = get_object_or_404(Sample, id=sample_id)
        previous_sample = samples.filter(id__lt=sample_id).order_by("id").last()
        next_sample = samples.filter(id__gt=sample_id).order_by("id").first()
        annotation = Annotation.objects.get_or_create(
            user=self.request.user,
            sample=sample,
            defaults={
                "pitch": PitchChoices.NONE.value,
                "secondary": SecondaryChoices.ADD_NONE.value,
            },
        )[0]
        annotation_form = AnnotationForm(instance=annotation)

        if not previous_sample:
            previous_sample = samples.order_by("id").last()

        if not next_sample:
            next_sample = samples.order_by("id").first()

        return {
            "num_samples": num_samples,
            "num_previous_samples": num_previous_samples,
            "sample": sample,
            "samples": samples,
            "previous_sample": previous_sample,
            "next_sample": next_sample,
            "annotation": annotation,
            "annotation_form": annotation_form,
            "navigation": navigation,
            "progress_percentage": f'{len([val for val in navigation.values() if val == "good-annotation"])/num_samples*100:.2f}',
            **context,
        }

    def post(self, request, *args, sample_id: int = None, **kwargs):
        sample = get_object_or_404(Sample, id=sample_id)
        annotation = get_object_or_404(Annotation, user=self.request.user, sample=sample)
        annotation_form = AnnotationForm(self.request.POST, instance=annotation)

        if annotation_form.is_valid():
            annotation_form.save()

        return redirect("annotate", sample_id=sample_id)
