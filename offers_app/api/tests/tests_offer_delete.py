"""
Tests for deleting offers in the offers_app.
"""

# 2. Drittanbieter (Third-Party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from offers_app.models import Offer


User = get_user_model()


class OfferDeleteSuccessTests(APITestCase):
    """
    Test suite for successful offer deletion.
    """

    def setUp(self):
        """
        Creates an owner and an offer for deletion tests.
        """
        self.owner = User.objects.create_user(
            username="owner",
            password="pass",
            type="business"
        )
        self.offer = Offer.objects.create(user=self.owner, title="Zu loeschen")
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_should_delete_own_offer_204(self):
        """
        Verifies that an owner can successfully delete their own offer.
        """
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)


class OfferDeleteErrorTests(APITestCase):
    """
    Test suite for offer deletion failures (Permissions & Auth).
    """

    def setUp(self):
        """
        Creates an owner, an intruder, and an offer.
        """
        self.owner = User.objects.create_user(
            username="owner",
            password="pass",
            type="business"
        )
        self.hacker = User.objects.create_user(
            username="hacker",
            password="pass",
            type="business"
        )
        self.offer = Offer.objects.create(user=self.owner, title="Test Offer")
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_should_return_403_when_hacker_deletes_offer(self):
        """
        Ensures that users cannot delete offers they do not own.
        """
        self.client.force_authenticate(user=self.hacker)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Offer.objects.count(), 1)

    def test_should_return_401_when_anonymous_deletes(self):
        """
        Ensures that unauthenticated users cannot delete offers.
        """
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
