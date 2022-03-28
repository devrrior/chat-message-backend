import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

application = ProtocolTypeRouter(
    {
        # 'http': get_asgi_application,
        'websocket': AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
