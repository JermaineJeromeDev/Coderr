# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from offer_app.models import Offer


User = get_user_model()


class OfferDeleteTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="pass", type="business")
        self.hacker = User.objects.create_user(username="hacker", password="pass", type="business")
        self.offer = Offer.objects.create(user=self.owner, title="Zu loeschen")
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_should_delete_own_offer_204(self):
        """Happy Path: Eigentümer löscht erfolgreich."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)

    def test_should_return_403_when_hacker_deletes_offer(self):
        """Unhappy Path: Fremder User darf nicht löschen."""
        self.client.force_authenticate(user=self.hacker)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Offer.objects.count(), 1)

    def test_should_return_401_when_anonymous_deletes(self):
        """Unhappy Path: Nicht eingeloggt."""
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)