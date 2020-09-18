from django.urls import re_path

# SSE install
from django.conf.urls import url
from channels.routing import URLRouter
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
import django_eventstream

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),

]

urlpatterns = [
    re_path(r'^events/(?P<room_name>\w+)/$', AuthMiddlewareStack(
        URLRouter(django_eventstream.routing.urlpatterns)
    ), {'channels': ['18c0']}),
    url(r'', AsgiHandler),
]