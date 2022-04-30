import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import Chat, Contact, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def fetch_messages(self, data):
        chat = self.get_chat_by_id(self.room_name)
        messages = chat.last_10_messages()

        content = {'command': 'messages', 'messages': self.messages_to_json(messages)}
        self.send_message(content)

    def new_message(self, data):
        contact = self.get_contact_by_user()
        chat = self.get_chat_by_id(self.room_name)
        message = Message.objects.create(
            contact=contact, content=data['message'], chat=chat
        )
        content = {'command': 'new_message', 'message': self.message_to_json(message)}
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

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def get_contact_by_user(self):
        return Contact.objects.get(user=self.scope['user'])

    def get_chat_by_id(self, chat_id):
        return Chat.objects.get(id=chat_id)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'chat_message', 'message': message}
        )

    def disconnect(self):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
