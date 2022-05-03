from rest_framework import serializers

from apps.chat.models import Chat, Contact, Message
from apps.user.api.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    contact = serializers.SerializerMethodField('get_contact_email')

    class Meta:
        model = Message
        fields = ('content', 'created_at', 'contact')

    def get_contact_email(self, obj):
        return obj.contact.user.email


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contact
        fields = ('user',)


class ChatSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField('get_last_message')
    receiver = serializers.SerializerMethodField('get_receiver')

    class Meta:
        model = Chat
        exclude = ('created_at', 'participants')

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.last()).data

    def get_receiver(self, obj):
        request = self.context.get('request', None)
        if request is not None and request.user.is_authenticated:
            if obj.participants.filter(user=request.user).exists():
                return UserSerializer(
                    obj.participants.exclude(user=request.user).first().user
                ).data
