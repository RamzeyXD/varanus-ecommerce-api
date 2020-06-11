from django.test import TestCase
from django.contrib.auth import get_user_model


class UserTests(TestCase):
    def test_user_create_correct(self):
        """Test creating a new user with an email correct"""
        email = 'test123@gmail.com'
        password = 'Testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_superuser_create_correct(self):
        """Test creating a new super user correct"""
        email = 'test123@gmail.com'
        password = 'Testpass123'

        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_new_user_email_normalized(self):
        """Test email to normalize"""
        email = 'test123@GMAIL.COM'
        user = get_user_model().objects.create_user(
            email=email,
            password='Test123'
        )

        self.assertEqual(user.email, email.lower())
