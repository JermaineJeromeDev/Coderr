# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from offer_app.models import Offer, OfferDetail
from orders_app.models import Order


User = get_user_model()


class OrderCreationSuccessTests(APITestCase):
    def setUp(self):
        self.biz = User.objects.create_user(username="biz", password="p", type="business")
        self.cust = User.objects.create_user(username="cust", password="p", type="customer")
        self.offer = Offer.objects.create(user=self.biz, title="Offer")
        self.detail = OfferDetail.objects.create(
            offer=self.offer, title="Basic", price=100, 
            delivery_time_in_days=5, offer_type="basic"
        )
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('order-list')

    def test_should_create_order_successfully_201(self):
        response = self.client.post(self.url, {"offer_detail_id": self.detail.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(response.data["price"], "100.00")


class OrderCreationErrorTests(APITestCase):
    def setUp(self):
        self.biz = User.objects.create_user(username="biz", password="p", type="business")
        self.cust = User.objects.create_user(username="cust", password="p", type="customer")
        self.url = reverse('order-list')

    def test_should_return_401_when_anonymous(self):
        response = self.client.post(self.url, {"offer_detail_id": 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_business_tries_to_order(self):
        self.client.force_authenticate(user=self.biz)
        response = self.client.post(self.url, {"offer_detail_id": 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_offer_detail_not_found(self):
        self.client.force_authenticate(user=self.cust)
        response = self.client.post(self.url, {"offer_detail_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_return_400_when_id_missing(self):
        self.client.force_authenticate(user=self.cust)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)