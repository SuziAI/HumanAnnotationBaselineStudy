from django.contrib import admin

from .models import Action, Annotation, Sample


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ("id", "real_name", "real_pitch", "real_secondary")
    search_fields = ("real_name", "real_pitch", "real_secondary")
    list_filter = ("real_pitch", "real_secondary")
    ordering = ("id",)


@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "sample", "pitch", "secondary")
    search_fields = ("user__username", "sample__real_name", "sample__real_pitch", "sample__real_secondary")
    list_filter = ("pitch", "secondary")
    raw_id_fields = ("user", "sample")
    ordering = ("id",)


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ("id", "annotation__user__username", "annotation", "timestamp")
    search_fields = (
        "annotation__user__username",
        "annotation__sample__real_name",
        "annotation__sample__real_pitch",
        "annotation__sample__real_secondary",
    )
    raw_id_fields = ("annotation",)
    ordering = ("-timestamp",)
