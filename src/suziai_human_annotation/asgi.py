import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suziai_human_annotation.settings.base")

application = get_asgi_application()
