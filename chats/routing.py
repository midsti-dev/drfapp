# chat/routing.py
from django.urls import re_path

from . import consumers
from .consumers import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/room/(?P<room_name>\w+)/$", ChatRoomConsumer.as_asgi()),
]

