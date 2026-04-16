# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from offer_app.models import Offer, OfferDetail


User = get_user_model()


class OfferDetailSuccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass", type="customer")
        self.offer = Offer.objects.create(user=self.user, title="Test Offer", description="Desc")
        OfferDetail.objects.create(offer=self.offer, title="D1", price=50, delivery_time_in_days=5, offer_type="basic")
        
        self.client.force_authenticate(user=self.user)
        self.url = reverse('offer-detail', kwargs={'pk': self.offer.pk})

    def test_should_return_offer_detail_with_correct_structure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.offer.id)
        self.assertIn("url", response.data["details"][0])
        self.assertEqual(response.data["min_price"], 50)


class OfferDetailErrorTests(APITestCase):
    def test_should_return_401_when_anonymous(self):
        url = reverse('offer-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_404_for_invalid_id(self):
        user = User.objects.create_user(username="tester2", password="pass")
        self.client.force_authenticate(user=user)
        url = reverse('offer-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)