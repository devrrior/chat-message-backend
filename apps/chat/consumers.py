import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Contact, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group for chat
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Join room group for notification
        self.room_name_personal = self.get_contact_by_user().id
        self.room_group_name_personal = 'notification_%s' % self.room_name_personal
        print('room_group_name_personal', self.room_group_name_personal)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name_personal, self.channel_name
        )

        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def fetch_messages(self, data):
        chat = self.get_chat_by_id(self.room_name)
        messages = chat.last_10_messages()
        print('messages', messages)
        content = {'command': 'messages', 'messages': self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        contact = self.get_contact_by_user()

        chat = self.get_chat_by_id(self.room_name)

        recipent = self.get_recipent(chat, contact.user)

        self.room_group_name_foreign = 'notification_%s' % recipent.id
        print('room_group_name_foreign', self.room_group_name_foreign)

        message = Message.objects.create(
            contact=contact, content=data['message'], chat=chat
        )
        content = {'command': 'new_message', 'message': self.message_to_json(message)}

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        content_for_notification = {
            'command': 'notification_message',
            'message': self.message_to_json(message),
        }
        content_for_notification['message']['chat_id'] = self.room_name
        self.send_notification(content_for_notification)

        return self.send_chat_message(content)

    # Serializers
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'contact': message.contact.user.email,
            'content': message.content,
            'created_at': str(message.created_at),
        }

    # Serializers

    commands = {'fetch_messages': fetch_messages, 'new_message': new_message}

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'chat.message', 'message': message}
        )

    def send_notification(self, message):
        # try:
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name_foreign,
            {'type': 'notification.message', 'message': message},
        )
        # except Exception as e:
        # print(e)

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def notification_message(self, event):
        message = event['message']

        try:
            # Send message to WebSocket
            self.send(text_data=json.dumps(message))
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name_foreign, self.channel_name
            )
        except Exception as e:
            print(e)

    def get_contact_by_user(self):
        return Contact.objects.get(user=self.scope['user'])

    def get_chat_by_id(self, chat_id):
        return Chat.objects.get(id=chat_id)

    def get_recipent(self, chat, sender):
        return chat.participants.exclude(user=sender).first()

    def disconnect(self):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
