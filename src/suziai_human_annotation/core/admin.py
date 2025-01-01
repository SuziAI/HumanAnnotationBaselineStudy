from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from .build_statistics import build_statistics
from .models import Action, Annotation, Sample

User = get_user_model()


class AdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        statistics = build_statistics()
        extra_context = extra_context or {}
        extra_context.update(
            {
                "statistics": statistics,
            }
        )
        return super().index(request, extra_context=extra_context)


core_admin_site = AdminSite(name="core")


@admin.register(Sample, site=core_admin_site)
class SampleAdmin(admin.ModelAdmin):
    list_display = ("id", "real_name", "real_pitch", "real_secondary", "group")
    search_fields = ("real_name", "real_pitch", "real_secondary", "group")
    list_filter = ("real_pitch", "real_secondary", "group")
    ordering = ("id",)


@admin.register(Annotation, site=core_admin_site)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "sample", "pitch", "secondary")
    search_fields = ("user__username", "sample__real_name", "sample__real_pitch", "sample__real_secondary")
    list_filter = ("pitch", "secondary")
    raw_id_fields = ("user", "sample")
    ordering = ("id",)


@admin.register(Action, site=core_admin_site)
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


core_admin_site.register(User, UserAdmin)
core_admin_site.register(Group, GroupAdmin)
