from django.urls import path, re_path
from django.conf.urls.static import static
from app_config import settings

from .views import *

urlpatterns = [
    path('', chat, name='chat'),
    re_path(r'^(?P<uuid>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})/$',
            chat_uuid, name='chat_uuid')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
