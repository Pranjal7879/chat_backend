# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
# django.setup() 

# import livechat.routing

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             livechat.routing.websocket_urlpatterns
#         )
#     ),
# })








from livechat.middleware import JWTAuthMiddleware
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.conf import settings
import os
import django
import livechat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            livechat.routing.websocket_urlpatterns
        )
    ),
})
