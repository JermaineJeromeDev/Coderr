# 2. Drittanbieter
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class OfferListSuccessTests(APITestCase):
    """Happy Path: Angebote auflisten."""
    def test_should_return_paginated_offer_list(self):
        url = reverse('offer-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)


class OfferListErrorTests(APITestCase):
    """Unhappy Path: Fehlerhafte Filter oder Parameter (400 Bad Request)."""
    def test_should_return_400_for_invalid_min_price_type(self):
        """Prüft, ob ein ungültiger Datentyp (String statt Float) abgefangen wird."""
        url = reverse('offer-list')
        response = self.client.get(url, {'min_price': 'viel_zu_teuer'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_400_for_invalid_ordering_field(self):
        """Prüft, ob Sortierung nach nicht existierenden Feldern abgelehnt wird."""
        url = reverse('offer-list')
        response = self.client.get(url, {'ordering': 'geheimnis'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)