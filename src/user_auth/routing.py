from django.urls import path
from src.user_auth import consumers
from app_config import settings
from django.conf.urls.static import static

websocket_urlpatterns = [
    path('ws/online_user/', consumers.OnlineUserConsumer.as_asgi())
]

if settings.DEBUG:
    websocket_urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
