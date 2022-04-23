from django.test import TestCase

from apps.user.models import User

from .models import Message


class MessageTestCase(TestCase):
    def test_message_creation(self):
        user1 = User.objects.create(email='devrrior@gmail.com', first_name='Fernando', last_name='Guerrero', password='password')
        message1 = Message.objects.create(author=user1, content='Hi mate!')
        self.assertEqual('Hi mate!', message1.content)
        self.assertEqual(user1, message1.author)
