# 2. Drittanbieter
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from offer_app.models import Offer
from reviews_app.models import Review


User = get_user_model()


class BaseInfoSuccessTests(APITestCase):
    
    def setUp(self):
        biz = User.objects.create_user(username="biz", type="business")
        cust = User.objects.create_user(username="cust", type="customer")
        Offer.objects.create(user=biz, title="Offer 1")
        Review.objects.create(business_user=biz, reviewer=cust, rating=4)
        Review.objects.create(business_user=biz, reviewer=cust, rating=5)
        self.url = reverse('base-info')

    def test_should_return_correct_statistics_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 2)
        self.assertEqual(response.data["average_rating"], 4.5)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)
