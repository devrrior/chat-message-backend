from django.test import TestCase

from apps.user.models import User

from .models import Message


class MessageTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='devrrior@gmail.com', first_name='Fernando', last_name='Guerrero', password='password')

    def test_message_creation(self):
        message1 = Message.objects.create(author=self.user, content='Hi mate!')
        self.assertEqual('Hi mate!', message1.content)
        self.assertEqual(self.user, message1.author)
