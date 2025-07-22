import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
import aioredis
from src import settings


# class RoomConsumer(
#     CreateModelMixin,
#     ObserverModelInstanceMixin,
#     GenericAsyncAPIConsumer
# ):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     lookup_field = "id"


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self, aioredis=None):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        user = self.scope["user"]
        redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        )

        # Определяем идентификатор
        if isinstance(user, AnonymousUser):
            self.user_id = f"anon_{self.channel_name}"
        else:
            self.user_id = f"user_{user.id}"

        await redis.sadd("active_users", self.user_id)
        await redis.close()

    async def disconnect(self, _):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        )
        await redis.srem("active_users", self.user_id)
        await redis.close()

    async def receive(self, text_data=None, bytes_data=None):
        # if not text_data:
        #     return
        #
        # try:
        #     data = json.loads(text_data)
        # except json.JSONDecodeError:
        #     await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
        #     return
        data = json.loads(text_data)
        message = data["message"]
        room = data["room"]
        user = self.scope["user"]
        username = user.username if not isinstance(user, AnonymousUser) else "Anonymous"
        await self.channel_layer.group_send(
            f"chat_{room}",
            {
                "type": "chat_message",
                "message": message,
                "room": room,
                "user": user,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        room = event["room"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "room": room,
                }
            )
        )
