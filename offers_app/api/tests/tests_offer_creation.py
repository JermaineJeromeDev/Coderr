"""
Tests for creating offers within the offers_app.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer


User = get_user_model()


class OfferCreationSuccessTests(APITestCase):
    """
    Test suite for successful offer creation by business users.
    """

    def setUp(self):
        """
        Sets up a business user and authenticates the client.
        """
        self.user = User.objects.create_user(
            username="biz_pro",
            password="password123",
            type="business"
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('offer-list')

    def test_should_create_offer_with_exactly_3_details(self):
        """
        Ensures an offer is created correctly when providing exactly 3 details.
        """
        data = {
            "title": "Grafikdesign-Paket",
            "description": "Umfassendes Paket",
            "details": [
                {
                    "title": "Basic",
                    "price": 100,
                    "delivery_time_in_days": 5,
                    "offer_type": "basic"
                },
                {
                    "title": "Standard",
                    "price": 200,
                    "delivery_time_in_days": 7,
                    "offer_type": "standard"
                },
                {
                    "title": "Premium",
                    "price": 500,
                    "delivery_time_in_days": 10,
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(len(response.data["details"]), 3)


class OfferCreationErrorTests(APITestCase):
    """
    Test suite for offer creation failures (Auth, Role, Validation).
    """

    def setUp(self):
        """
        Creates a customer and a business user for permission testing.
        """
        self.customer = User.objects.create_user(
            username="customer",
            password="pass",
            type="customer"
        )
        self.business = User.objects.create_user(
            username="business",
            password="pass",
            type="business"
        )
        self.url = reverse('offer-list')

    def test_should_return_403_when_customer_tries_to_create(self):
        """
        Ensures that customers are forbidden from creating offers.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(self.url, {"title": "Test"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_401_when_not_logged_in(self):
        """
        Ensures that unauthenticated users cannot create offers.
        """
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {"title": "Test"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_400_when_details_are_missing(self):
        """
        Verifies that missing details result in a 400 Bad Request.
        """
        self.client.force_authenticate(user=self.business)
        data = {"title": "No Details", "description": "Fail"}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_when_not_exactly_3_details(self):
        """
        Ensures that having fewer or more than 3 details is rejected.
        """
        self.client.force_authenticate(user=self.business)
        data = {
            "title": "Wrong Count",
            "details": [
                {
                    "title": "Only One",
                    "price": 10,
                    "delivery_time_in_days": 1,
                    "offer_type": "basic"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)