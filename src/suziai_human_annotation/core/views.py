from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from suziai_human_annotation.core.models import Annotation, Sample


class AnnotateView(LoginRequiredMixin, TemplateView):
    template_name = "suziai_human_annotation/core/annotate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_samples = Sample.objects.all().count()
        default_current_id = Annotation.objects.aggregate(max_sample_id=Max("sample__id"))["max_sample_id"]

        current_id = kwargs.get("current_id", default_current_id)
        current_sample = get_object_or_404(Sample, id=current_id)
        current_idx = Sample.objects.filter(id__lt=current_id).count()

        min_id = Sample.objects.filter(id__lt=current_sample.id).order_by("-id").last()
        min_id = min_id.id if min_id else None
        previous_id = Sample.objects.filter(id__lt=current_sample.id).order_by("-id").first()
        next_id = Sample.objects.filter(id__gt=current_sample.id).order_by("id").first()
        max_id = Sample.objects.filter(id__gt=current_sample.id).order_by("id").last()
        max_id = max_id.id if max_id else None

        previous_id = previous_id.id if previous_id else max_id
        next_id = next_id.id if next_id else min_id

        context["current_sample_display"] = f"{current_idx+1} / {num_samples}"
        context["sample_image"] = current_sample.image.url
        context["previous_id"] = previous_id
        context["next_id"] = next_id
        return context
