from django.apps import AppConfig
from django.db.models.signals import post_save


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "suziai_human_annotation.core"

    def ready(self):
        from suziai_human_annotation.core.models import Annotation
        from suziai_human_annotation.core.models.signals import create_action_on_annotation_save

        post_save.connect(create_action_on_annotation_save, sender=Annotation)
