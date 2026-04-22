"""
Tests for updating offers (PATCH) in the offers_app.
"""

# 2. Drittanbieter (Third-Party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OfferPatchSuccessTests(APITestCase):
    """
    Test suite for successful offer updates.
    """

    def setUp(self):
        """
        Sets up an owner, an offer, and an offer detail for patching.
        """
        self.user = User.objects.create_user(
            username="owner",
            password="pass",
            type="business"
        )
        self.offer = Offer.objects.create(user=self.user, title="Alt")
        OfferDetail.objects.create(
            offer=self.offer,
            title="D1",
            price=100,
            delivery_time_in_days=5,
            offer_type="basic"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_should_update_successfully_200(self):
        """
        Ensures an owner can update their offer title.
        """
        response = self.client.patch(self.url, {"title": "Neu"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Neu")


class OfferPatchErrorTests(APITestCase):
    """
    Test suite for offer update failure scenarios (Auth, Permissions, Data).
    """

    def setUp(self):
        """
        Creates an owner, an unauthorized user, and a target offer.
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
        self.offer = Offer.objects.create(user=self.owner, title="Test")
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_should_return_401_if_not_logged_in(self):
        """
        Verifies that unauthenticated users cannot patch offers.
        """
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, {"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_if_not_owner(self):
        """
        Ensures that users cannot patch offers they do not own.
        """
        self.client.force_authenticate(user=self.hacker)
        response = self.client.patch(self.url, {"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_if_not_found(self):
        """
        Verifies that patching a non-existent offer ID returns 404.
        """
        self.client.force_authenticate(user=self.owner)
        url = reverse('offer-detail', kwargs={'pk': 9999})
        response = self.client.patch(url, {"title": "Neu"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_400_for_invalid_data(self):
        """
        Ensures that invalid payload results in a 400 Bad Request.
        """
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url, {"title": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
