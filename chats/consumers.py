import json

from channels.generic.websocket import AsyncWebsocketConsumer

# class RoomConsumer(
#     CreateModelMixin,
#     ObserverModelInstanceMixin,
#     GenericAsyncAPIConsumer
# ):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer
#     lookup_field = "id"


class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, _):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

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
        await self.channel_layer.group_send(
            f"chat_{room}",
            {
                "type": "chat_message",
                "message": message,
                "room": room,
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
