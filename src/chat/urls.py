from django.urls import path
from django.conf.urls.static import static
from app_config import settings

from .views import *

urlpatterns = [
    path('', chat, name='chat'),
    path('<str:uuid>/', chat_uuid, name='chat_uuid'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
