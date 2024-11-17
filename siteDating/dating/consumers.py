from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
import json

class LikesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Проверяем, что пользователь аутентифицирован
        if self.scope["user"] == AnonymousUser():
            await self.close()  # Закрываем соединение для анонимных пользователей
            return

        self.user = self.scope["user"]
        self.group_name = f"user_{self.user.id}_likes"

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы, если group_name был инициализирован
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        # Обрабатываем входящие сообщения (если нужно)
        pass

    async def send_like_update(self, event):
        # Проверяем, что group_name был инициализирован перед отправкой данных
        if hasattr(self, 'group_name'):
            # Отправляем обновление на фронтенд
            await self.send(text_data=json.dumps({
                "type": "like_update",
                "data": event["data"]
            }))
