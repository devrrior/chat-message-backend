from django.db import models

from apps.user.models import User

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'"{self.content}" by {self.author.email}'

    def last_10_messages():
        return Message.objects.order_by('-created_at').all()[:10]
