from django.db import models

from apps.user.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    friends = models.ForeignKey('self', related_name='friends', blank=True)

    def __str__(self):
        return self.user.email


class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Chat between {self.participants.all()}'

    def last_10_messages(self):
        return self.messages.order_by('-created_at').all()[:30]

    def last_message(self):
        return self.messages.order_by('-created_at').first()


class Message(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.content}" by {self.contact.user.email}'
