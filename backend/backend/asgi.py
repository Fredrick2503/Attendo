"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# application = get_asgi_application()

# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from client_api import routing

# routing the asgi 
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        #  "websocket": URLRouter(routing.ws_urlpattern),
         "websocket": AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(routing.ws_urlpattern))),
    }
)
