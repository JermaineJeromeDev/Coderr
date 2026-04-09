from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class LoginSuccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            password = "password123",
            email = "test@mail.de"
        )

    def test_login_success(self):
        url = reverse('login')
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@mail.de")
        self.assertEqual(response.data["user_id"], self.user.id)


class LoginErrorTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="password123")
        self.url = reverse('login')

    def test_should_return_400_for_wrong_password(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_for_non_existing_user(self):
        data = {"username": "unknown", "password": "password123"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)