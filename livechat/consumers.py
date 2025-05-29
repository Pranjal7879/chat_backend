import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

connected_users = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:

            token = self.scope['query_string'].decode().split('=')[1]
            access_token = AccessToken(token)
            user = await self.get_user(access_token['user_id'])
            self.scope['user'] = user
            self.user = user
        except Exception as e:
            print(f"[Connect Error] Invalid token or user: {e}")
            await self.close()
            return


        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"


        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


        connected_users[self.user.email] = self.channel_name
        print(f"[Connected] {self.user.email} joined {self.room_group_name}")

   
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "users_update",
                "users": list(connected_users.keys()),
            }
        )

    async def disconnect(self, close_code):
      
        if self.user and self.user.email in connected_users:
            del connected_users[self.user.email]

           
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "users_update",
                    "users": list(connected_users.keys()),
                }
            )

      
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"[Disconnected] {self.user.email} left {self.room_group_name}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            to_user_email = data.get("to")
            if not message or not to_user_email:
                print("[Receive Warning] Missing 'message' or 'to'")
                return
        except json.JSONDecodeError as e:
            print(f"[Receive Error] Invalid JSON: {e}")
            return

      
        if to_user_email in connected_users:
            await self.channel_layer.send(
                connected_users[to_user_email],
                {
                    "type": "chat.message",
                    "message": message,
                    "from": self.user.email,
                    "to": to_user_email,
                }
            )

       
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": message,
            "from": "You",
            "to": to_user_email,
        }))


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "from": event["from"],
            "to": event["to"],
        }))


    async def users_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "users",
            "users": event["users"],
        }))

    @staticmethod
    @database_sync_to_async
    def get_user(user_id):
        return User.objects.get(id=user_id)




















