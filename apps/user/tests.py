from django.test import TestCase
from .models import User

class UserTestCase(TestCase):
    def test_create_user(self):
        user1 = User.objects.create(email='devrrior@gmail.com', first_name='Fernando', last_name='Guerrero', password='password')
        self.assertEqual(user1.email, 'devrrior@gmail.com')
        self.assertEqual(user1.first_name, 'Fernando')
        self.assertEqual(user1.last_name, 'Guerrero')
