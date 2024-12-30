from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from suziai_human_annotation.core.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello-world/", HomePageView.as_view(), name="home"),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

try:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
except ImportError:
    pass
