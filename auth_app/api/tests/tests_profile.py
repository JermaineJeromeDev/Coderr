from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()

class ProfileDetailSuccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", 
            password="password123",
            type="customer",
            email="test@mail.de"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('profile-detail', kwargs={'pk': self.user.pk})

    def test_should_return_200_and_correct_username(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "tester")

    def test_should_return_empty_strings_for_unset_fields(self):
        """Prüft DoD: Felder wie location/tel dürfen nicht null sein."""
        response = self.client.get(self.url)
        # Diese Tests werden aktuell fehlschlagen (RED), da die Felder im Model fehlen
        self.assertEqual(response.data["location"], "")
        self.assertEqual(response.data["tel"], "")


class ProfileDetailErrorTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="password123")
        self.url = reverse('profile-detail', kwargs={'pk': self.user.pk})

    def test_should_return_401_if_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_404_if_profile_does_not_exist(self):
        self.client.force_authenticate(user=self.user)
        # Eine ID nutzen, die sicher nicht existiert
        url = reverse('profile-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
