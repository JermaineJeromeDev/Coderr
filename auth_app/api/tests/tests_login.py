"""
Tests for the authentication login endpoint.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class LoginSuccessTests(APITestCase):
    """
    Test suite for successful user authentication.
    """

    def setUp(self):
        """
        Creates a test user for authentication checks.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="test@mail.de"
        )

    def test_login_success(self):
        """
        Ensures that a user can login with valid credentials 
        and receives a token plus user details.
        """
        url = reverse('login')
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@mail.de")
        self.assertEqual(response.data["user_id"], self.user.id)


class LoginErrorTests(APITestCase):
    """
    Test suite for failed authentication scenarios.
    """

    def setUp(self):
        """
        Sets up the environment for error testing.
        """
        User.objects.create_user(username="testuser", password="password123")
        self.url = reverse('login')

    def test_should_return_400_for_wrong_password(self):
        """
        Verifies that an incorrect password results in a 400 Bad Request.
        """
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_for_non_existing_user(self):
        """
        Verifies that a non-existing username results in a 400 Bad Request.
        """
        data = {"username": "unknown", "password": "password123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
