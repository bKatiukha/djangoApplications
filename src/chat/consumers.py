import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.utils.timesince import timesince

from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('try to connect chat')
        self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
        self.room_group_name = f'chat_{self.room_uuid}'

        room = await sync_to_async(self.get_room_by_uuid)(self.room_uuid)

        if room is None:
            print(f'Room with UUID {self.room_uuid} does not exist.')
            await self.close()
            return

        print('Join room group', self.room_uuid)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    def get_room_by_uuid(self, room_uuid):
        try:
            return Room.objects.get(uuid=room_uuid)
        except Room.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json['type']

        # Send message to room group
        if event_type == 'chat_message':
            print('new_message', text_data_json['data']['message'])
            message = text_data_json['data']['message']
            created_by = text_data_json['data']['created_by']

            new_message = await self.save_message(created_by, message)
            print('new_message', new_message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'data': {
                        'message': message,
                        'created_by': created_by,
                        # 'created_at': timesince(new_message.created_at)
                    }
                }
            )

    @database_sync_to_async
    def save_message(self, created_by, message):
        # save message in bd
        message = Message.objects.create(
            message=message,
            created_by=User.objects.get(username=created_by),
            room=Room.objects.get(uuid=self.room_uuid)
        )
        room = Room.objects.get(uuid=self.room_uuid)
        room.messages.add(message)

    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'data': event['data']
        }))

