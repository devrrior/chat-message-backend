import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from apps.chat.middleware import TokenAuthMiddleware
from apps.chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = ProtocolTypeRouter(
    {
        # 'http': get_asgi_application,
        'websocket': TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
