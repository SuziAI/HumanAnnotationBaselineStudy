from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from suziai_human_annotation.core.admin import core_admin_site
from suziai_human_annotation.core.views import *

urlpatterns = [
    path("admin/", core_admin_site.urls),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="./suziai_human_annotation/core/login.html"), name="login"
    ),
    path("annotate/<int:sample_id>/", AnnotateView.as_view(), name="annotate"),
    path("", DefaultView.as_view(), name="default"),
    path("download_statistics/", DownloadStatisticsView.as_view(), name="download-statistics"),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

try:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
except ImportError:
    pass
