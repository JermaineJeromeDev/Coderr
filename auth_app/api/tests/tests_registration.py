# 2. Drittanbieter
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class RegistrationSuccessTests(APITestCase):
    def test_should_create_user_and_return_token_and_custom_data(self):
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
    """Tests für alle Fehlerfälle (Unhappy Path)."""

    def test_should_return_400_if_passwords_dont_match(self):
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
        url = reverse('registration')
        data = {"username": "tester", "email": "test@coderr.com", "type": "customer"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_when_username_already_exists(self):
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
