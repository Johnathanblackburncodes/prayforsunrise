from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import main_app.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'http': URLRouter(main_app.routing.urlpatterns),

    'websocket': AuthMiddlewareStack(
        URLRouter(
            main_app.routing.websocket_urlpatterns
        )
    ),
})