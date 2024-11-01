"""
ASGI config for app_config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from src.web_rtc import routing as web_rtc_routing
from src.chat import routing as chat_routing
from src.user_auth import routing as auth_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            auth_routing.websocket_urlpatterns +
            chat_routing.websocket_urlpatterns +
            web_rtc_routing.websocket_urlpatterns
        )
    )
})
