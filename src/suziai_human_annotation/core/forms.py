from django import forms

from suziai_human_annotation.core.models import Annotation
from suziai_human_annotation.core.models.choices import PitchChoices, SecondaryChoices


class AnnotationForm(forms.ModelForm):
    class Meta:
        model = Annotation
        fields = ["pitch", "secondary"]

    pitch = forms.ChoiceField(
        choices=PitchChoices.choices,
    )

    secondary = forms.ChoiceField(
        choices=SecondaryChoices.choices,
    )
