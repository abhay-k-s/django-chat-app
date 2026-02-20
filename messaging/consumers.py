import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user = self.scope["user"]
        self.other_user_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        user1 = self.user.id
        user2 = self.other_user_id
        self.room_name = f"chat_{min(user1, user2)}_{max(user1, user2)}"

        await self.channel_layer.group_add(self.room_name,self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name,self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        receiver = await sync_to_async(User.objects.get)(id=self.other_user_id)
        msg = await sync_to_async(Message.objects.create)(sender=self.user,receiver=receiver,content=message)

        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "sender_id": self.user.id,
                "message": message,
                "message_id": msg.id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "chat","sender_id": event["sender_id"],"message": event["message"],"message_id": event["message_id"],}))

    async def mark_read(self, event):
        await self.send(text_data=json.dumps({"type": "read","sender_id": event["sender_id"],}))