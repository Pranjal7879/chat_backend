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















import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import livechat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            livechat.routing.websocket_urlpatterns
        )
    ),
})

