"""
Tests for listing and filtering offers in the offers_app.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer


User = get_user_model()


class OfferListSuccessTests(APITestCase):
    """
    Test suite for successful offer listing and pagination.
    """

    def setUp(self):
        """
        Creates a seller and a test offer.
        """
        self.user = User.objects.create_user(
            username="seller",
            password="pass",
            type="business"
        )
        Offer.objects.create(
            user=self.user,
            title="Test Offer",
            description="Desc"
        )
        self.url = reverse('offer-list')

    def test_should_return_paginated_offer_list(self):
        """
        Ensures the offer list is returned with the correct pagination structure.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)


class OfferListErrorTests(APITestCase):
    """
    Test suite for offer list filtering and ordering errors.
    """

    def test_should_return_400_for_invalid_min_price_type(self):
        """
        Verifies that providing a non-numeric min_price results in a 400 error.
        """
        url = reverse('offer-list')
        response = self.client.get(url, {'min_price': 'not-a-number'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_for_invalid_ordering_field(self):
        """
        Verifies that ordering by an invalid field results in a 400 error.
        """
        url = reverse('offer-list')
        response = self.client.get(url, {'ordering': 'invalid_field'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)