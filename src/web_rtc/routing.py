from django.urls import path
from src.web_rtc import consumers

websocket_urlpatterns = [
    path('ws/call/', consumers.CallConsumer.as_asgi())
]
