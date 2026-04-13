from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer_app.models import Offer


User = get_user_model()


class OfferListSuccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="seller", password="pass", type="business")
        Offer.objects.create(user=self.user, title="Test Offer", description="Desc")
        self.url = reverse('offer-list')

    def test_should_return_paginated_offer_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)


class OfferListErrorTests(APITestCase):
    def test_should_return_400_for_invalid_min_price_type(self):
        url = reverse('offer-list')
        response = self.client.get(url, {'min_price': 'not-a-number'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_for_invalid_ordering_field(self):
        url = reverse('offer-list')
        response = self.client.get(url, {'ordering': 'invalid_field'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)