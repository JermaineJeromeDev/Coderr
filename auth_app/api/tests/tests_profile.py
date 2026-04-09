from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class ProfileUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = "testuser",
            password = "password123",
            type = "business"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('profile-detail', kwargs={'pk': self.user.pk})

    def test_should_update_profile_fields(self):
        data = {
            "first_name": "Max",
            "location": "Berlin",
            "tel": "123456789"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["location"], "Berlin")
        self.assertEqual(response.data["first_name"], "Max")

    def test_fields_should_be_empty_string_not_null(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data["location"], "")


