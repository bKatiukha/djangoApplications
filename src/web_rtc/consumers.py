import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CallConsumer(WebsocketConsumer):

    # Websocket connected with client
    def connect(self):
        self.accept()
        print('connect')
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
        async_to_sync(self.channel_layer.group_discard)(
            self.my_name,
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
            self.my_name = name

            # Join room
            async_to_sync(self.channel_layer.group_add)(
                self.my_name,
                self.channel_name
            )

        # on call to other user message
        if event_type == 'offer':
            name = text_data_json['data']['name']
            print(self.my_name, "is calling", name)

            # to notify the callee we sent an event to the group name
            # and theirs group name is the name
            async_to_sync(self.channel_layer.group_send)(
                name,
                {
                    'type': 'offer',
                    'data': {
                        'caller': self.my_name,
                        'avatar': text_data_json['data']['avatar'],
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        # on call was answered
        if event_type == 'answer':
            # has received call from someone now notify the calling user
            # we can notify to the group with the caller name

            caller = text_data_json['data']['caller']

            async_to_sync(self.channel_layer.group_send)(
                caller,
                {
                    'type': 'answer',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if event_type == 'candidate':
            print('candidate')
            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'candidate',
                    'data': {
                        'rtcMessage': text_data_json['data']['rtcMessage']
                    }
                }
            )

        if event_type == 'declineCall':
            print('decline call')
            user = text_data_json['data']['user']

            async_to_sync(self.channel_layer.group_send)(
                user,
                {
                    'type': 'declineCall',
                    'data': {}
                }
            )

    # send RTCDescription to callee
    def offer(self, event):

        print('Call received by ', self.my_name)
        self.send(text_data=json.dumps({
            'type': 'offer',
            'data': event['data']
        }))

    # send RTCDescription to caller to create p2p connection
    def answer(self, event):

        print("Call answered by", self.my_name)
        self.send(text_data=json.dumps({
            'type': 'answer',
            'data': event['data']
        }))

    # send ICE candidate to caller
    def candidate(self, event):
        print('Candidate ', event['data'])
        self.send(text_data=json.dumps({
            'type': 'candidate',
            'data': event['data']
        }))

    # decline call
    def declineCall(self, event):
        print('declineCall ')
        self.send(text_data=json.dumps({
            'type': 'declineCall',
            'data': event['data']
        }))
