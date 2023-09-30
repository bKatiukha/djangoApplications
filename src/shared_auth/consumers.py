import json
import threading

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q

from src.shared_auth.models import UserProfile


class OnlineUserConsumer(WebsocketConsumer):
    room_name = 'OnlineUserConsumer'
    user_name = ''

    # Websocket connected with client
    def connect(self):
        self.accept()
        # response to client, that we are connected.
        self.send(text_data=json.dumps({
            'type': 'connection',
            'data': {
                'message': "Connected"
            }
        }))

    def disconnect(self, close_code):
        # Leave room group
        print('disconnect')
        if self.user_name:
            try:
                def user_left_task():
                    user_profile = UserProfile.objects.get(user__username=self.user_name)
                    user_profile.online_status -= 1
                    user_profile.save()
                    if user_profile.online_status == 0:
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_name,
                            {
                                'type': 'user_left',
                                'data': {
                                    'username': user_profile.user.username,
                                }
                            }
                        )

                # Create the timer thread with the user_left_task function
                left_timer_thread = threading.Timer(5, user_left_task)
                left_timer_thread.start()
            except UserProfile.DoesNotExist:
                print('no user with name: ', self.user_name)

            async_to_sync(self.channel_layer.group_discard)(
                self.room_name,
                self.channel_name
            )

    # User messages from client WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('receive', text_data)
        event_type = text_data_json['type']

        # on login message
        if event_type == 'login':
            name = text_data_json['data']['name']

            # we will use this as room name as well
            self.user_name = name
            if self.user_name:
                print('name', name)
                try:
                    user_profile = UserProfile.objects.get(user__username=name)
                    user_profile.online_status += 1
                    user_profile.save()
                    if user_profile.online_status == 1:
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_name,
                            {
                                'type': 'user_in',
                                'data': {
                                    'user': {
                                        'username': user_profile.user.username,
                                        'avatar': user_profile.avatar.url
                                    },
                                }
                            }
                        )

                except UserProfile.DoesNotExist:
                    print('no user with name: ', name)

                # Join room
                async_to_sync(self.channel_layer.group_add)(
                    self.room_name,
                    self.channel_name
                )

        if event_type == 'get_online_users':
            condition = Q(online_status__gt=0) & ~Q(user__username=self.user_name)
            online_users = list(UserProfile.objects.filter(condition).values('user__username', 'avatar'))
            online_users_data = [{
                'username': user['user__username'],
                'avatar': '/media/' + user['avatar']
             } for user in online_users]

            self.send(text_data=json.dumps({
                'type': 'online_users',
                'data': {'online_users': online_users_data}
            }))

    def user_left(self, event):
        self.send(text_data=json.dumps({
            'type': 'user_left',
            'data': event['data']
        }))

    def user_in(self, event):
        self.send(text_data=json.dumps({
            'type': 'user_in',
            'data': event['data']
        }))

