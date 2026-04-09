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
        response = self.client.get(self.url)
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
        url = reverse('profile-detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfileUpdateSuccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="pass123")
        self.client.force_authenticate(user=self.user)
        self.url = reverse('profile-detail', kwargs={'pk': self.user.pk})

    def test_should_update_own_profile_successfully(self):
        data = {"first_name": "Max", "location": "Berlin"}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Max")
        self.assertEqual(response.data["location"], "Berlin")


class ProfileUpdateErrorTests(APITestCase):
    """Unhappy Path: Permission & Auth Fehler (401, 403, 404)."""
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass123")
        self.hacker = User.objects.create_user(username="hacker", password="pass123")
        self.url_owner = reverse('profile-detail', kwargs={'pk': self.owner.pk})

    def test_should_return_401_when_not_authenticated(self):
        """DoD: 401 bei fehlendem Login."""
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url_owner, {"first_name": "Anon"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_editing_foreign_profile(self):
        """DoD: 403 wenn nicht der Eigentümer."""
        self.client.force_authenticate(user=self.hacker)
        response = self.client.patch(self.url_owner, {"first_name": "Evil"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_if_profile_not_found(self):
        """DoD: 404 bei ungültiger ID."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('profile-detail', kwargs={'pk': 99999})
        response = self.client.patch(url, {"first_name": "Niemand"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)