import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels_redis.core import RedisChannelLayer

from django.utils import timezone

from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.user = self.scope['user']
        self.scope: dict
        self.channel_layer: RedisChannelLayer

        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        
        await self.channel_layer.group_add(group=self.room_group_name, channel=self.channel_name)
        
        await self.accept()

    async def disconnect(self, code) -> None:
        await self.channel_layer.group_discard(group=self.room_group_name, channel=self.channel_name)

    async def persist_message(self, message) -> None:
        await Message.objects.acreate(user=self.user, course_id=self.id, content=message)

    async def receive(self, text_data=None, bytes_data=None) -> None:
        text_data_json: dict = json.loads(s=text_data)
        message = text_data_json['message']
        now = timezone.now()

        await self.channel_layer.group_send(group=self.room_group_name, message=dict(type='chat_message', message=message, user=self.user.username, datetime=now.isoformat()))

        await self.persist_message(message=message)

    async def chat_message(self, event) -> None:
        await self.send(text_data=json.dumps(event))