from django.test import TestCase

from apps.user.models import User

from .models import Chat, Contact, Message


class ContactTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='devrrior@gmail.com',
            first_name='Fernando',
            last_name='Guerrero',
            password='password',
        )

    def test_contact_creation(self):
        contact = Contact.objects.create(user=self.user)
        self.assertTrue(isinstance(contact, Contact))
        self.assertEqual(self.user, contact.user)


class ChatTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(
            email='devrrior@gmail.com',
            first_name='Fernando',
            last_name='Guerrero',
            password='password1',
        )
        self.contact1 = Contact.objects.create(user=user1)

        user2 = User.objects.create(
            email='k1rie@gmail.com',
            first_name='Diego',
            last_name='Gonzalez',
            password='password2',
        )
        self.contact2 = Contact.objects.create(user=user2)

    def test_chat_creation(self):
        chat = Chat.objects.create()

        chat.participants.set([self.contact1, self.contact2])

        self.assertTrue(isinstance(chat, Chat))
        self.assertEqual(chat.participants.count(), 2)
        self.assertEqual(chat.messages.count(), 0)


class MessageTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(
            email='devrrior@gmail.com',
            first_name='Fernando',
            last_name='Guerrero',
            password='password',
        )
        self.contact = Contact.objects.create(user=user)
        self.chat = Chat.objects.create()
        self.chat.participants.set([self.contact])

    def test_message_creation(self):
        message = Message.objects.create(contact=self.contact, content='Hi mate!', chat=self.chat)

        self.assertTrue(isinstance(message, Message))
        self.assertEqual('Hi mate!', message.content)
        self.assertEqual(self.contact, message.contact)
