from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Action, Annotation


@receiver(post_save, sender=Annotation)
def create_action_on_annotation_save(sender, instance, created, **kwargs):
    """
    Automatically creates an Action instance whenever an Annotation is saved.

    Args:
        sender: The model class that triggered the signal.
        instance: The actual instance of the model being saved.
        created: Boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """

    Action.objects.create(annotation=instance)
