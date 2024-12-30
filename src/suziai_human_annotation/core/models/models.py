from django.contrib.auth import get_user_model
from django.db import models

from .choices import PitchChoices, SecondaryChoices
from .files import filename_generator


class Sample(models.Model):
    image = models.ImageField(upload_to=filename_generator("samples/"))
    real_name = models.CharField(max_length=128, unique=True)
    real_pitch = models.CharField(max_length=16, choices=PitchChoices.choices)
    real_secondary = models.CharField(max_length=16, choices=SecondaryChoices.choices)


class Annotation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="annotations")
    sample = models.ForeignKey("Sample", on_delete=models.CASCADE, related_name="annotations")
    pitch = models.CharField(max_length=16, choices=PitchChoices.choices)
    secondary = models.CharField(max_length=16, choices=SecondaryChoices.choices)

    class Meta:
        unique_together = ("user", "sample")


class Action(models.Model):
    annotation = models.ForeignKey("Annotation", on_delete=models.CASCADE, related_name="actions")
    timestamp = models.DateTimeField(auto_now_add=True)
