"""
Tests for the user registration endpoint.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class RegistrationSuccessTests(APITestCase):
    """
    Test suite for successful user registration.
    """

    def test_should_create_user_and_return_token_and_custom_data(self):
        """
        Ensures a user can be created with valid data and receives 
        an authentication token along with user information.
        """
        url = reverse('registration')
        data = {
            "username": "tester",
            "email": "test@coderr.com",
            "password": "safe-password-123",
            "repeated_password": "safe-password-123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "tester")
        self.assertIn("user_id", response.data)


class RegistrationErrorTests(APITestCase):
    """
    Test suite for various registration failure scenarios (Unhappy Path).
    """

    def test_should_return_400_if_passwords_dont_match(self):
        """
        Verifies that registration fails if the password and 
        repeated password do not match.
        """
        url = reverse('registration')
        data = {
            "username": "tester",
            "email": "test@coderr.com",
            "password": "password123",
            "repeated_password": "wrongpassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_should_return_400_when_password_is_missing(self):
        """
        Verifies that registration fails if the password field is missing.
        """
        url = reverse('registration')
        data = {"username": "tester", "email": "test@coderr.com", "type": "customer"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_when_username_already_exists(self):
        """
        Ensures that registration fails if the username is already taken.
        """
        User.objects.create_user(username="existinguser", password="password123")
        url = reverse('registration')
        data = {
            "username": "existinguser",
            "email": "unique@mail.de",
            "password": "newpassword123",
            "repeated_password": "newpassword123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_when_email_is_invalid(self):
        """
        Verifies that an invalid email format results in a 400 Bad Request.
        """
        url = reverse('registration')
        data = {
            "username": "tester",
            "email": "keine-email",
            "password": "password123",
            "repeated_password": "password123",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
