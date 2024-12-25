from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
import json
from asgiref.sync import sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
import uuid


class LikesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            print(f"User {self.scope['user'].id} is authenticated.")
            self.group_name = f"user_{self.scope['user'].id}_likes"
        else:
            print("Anonymous user connected.")
            self.group_name = "anonymous_likes"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "unknown")

            if message_type == "authenticate":
                token = data.get("token")
                if not token:
                    await self.send(text_data=json.dumps({
                        "type": "error",
                        "data": "Authentication failed: Token is missing."
                    }))
                    return

                try:
                    decoded_token = AccessToken(token)
                    user_id = decoded_token["user_id"]

                    try:
                        user_id = uuid.UUID(user_id)
                    except ValueError:
                        await self.send(text_data=json.dumps({
                            "type": "error",
                            "data": "Authentication failed: Invalid user ID format."
                        }))
                        return

                    User = get_user_model()
                    user = await sync_to_async(User.objects.get)(id=user_id)


                    self.scope["user"] = user
                    self.group_name = f"user_{str(user.id)}_likes"
                    await self.channel_layer.group_add(
                        self.group_name,
                        self.channel_name
                    )
                    await self.send(text_data=json.dumps({
                        "type": "authenticate_response",
                        "data": "Authentication successful."
                    }))
                except Exception as e:
                    await self.send(text_data=json.dumps({
                        "type": "error",
                        "data": f"Authentication failed: {str(e)}"
                    }))
            elif message_type == "like_status":
                response = {
                    "type": "like_status_response",
                    "data": {
                        "message": "This is a response for your like status request.",
                        "status": "anonymous" if not self.scope["user"].is_authenticated else "authenticated"
                    }
                }
                await self.send(text_data=json.dumps(response))
            else:
                await self.send(text_data=json.dumps({
                    "type": "error",
                    "data": "Unknown message type."
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "type": "error",
                "data": "Invalid JSON format."
            }))

    async def send_like_update(self, event):
        # Отправка обновлений о лайках
        print('hasattr(self, "group_name"):', hasattr(self, 'group_name'))
        if hasattr(self, 'group_name'):
            # Отправка сообщения всем пользователям в группе
            event_data = event["data"]


            if isinstance(event_data, dict):
                event_data = {key: (str(value) if isinstance(value, uuid.UUID) else value) for key, value in event_data.items()}

            await self.send(text_data=json.dumps({
                "type": "like_update",
                "data": event_data
            }))