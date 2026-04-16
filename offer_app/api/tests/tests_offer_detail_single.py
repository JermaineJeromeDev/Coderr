# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from offer_app.models import Offer, OfferDetail


User = get_user_model()


class OfferDetailSingleSuccessTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.offer = Offer.objects.create(user=self.user, title="Offer")
        self.detail = OfferDetail.objects.create(
            offer=self.offer, title="Basic", price=100, 
            delivery_time_in_days=5, offer_type="basic",
            features=["Feature 1"]
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('offer-detail-single', kwargs={'pk': self.detail.pk})

    def test_should_return_single_detail_data_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Basic")
        self.assertEqual(response.data["offer_type"], "basic")


class OfferDetailSingleErrorTests(APITestCase):
    def test_should_return_401_when_anonymous(self):
        url = reverse('offer-detail-single', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)