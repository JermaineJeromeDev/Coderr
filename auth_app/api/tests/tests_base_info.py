"""
Tests for the BaseInfo aggregate endpoint.
"""

# 2. Drittanbieter (Third-party)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# 3. Lokale Importe
from offers_app.models import Offer
from reviews_app.models import Review


User = get_user_model()


class BaseInfoSuccessTests(APITestCase):
    """
    Test suite for successful retrieval of platform-wide statistics.
    """

    def setUp(self):
        """
        Creates a business user, two customers, one offer, and two reviews
        to provide a basis for aggregate statistics.
        """
        biz = User.objects.create_user(username="biz", type="business")
        cust1 = User.objects.create_user(username="cust1", type="customer")
        cust2 = User.objects.create_user(username="cust2", type="customer")
        Offer.objects.create(user=biz, title="Offer 1")
        Review.objects.create(business_user=biz, reviewer=cust1, rating=4)
        Review.objects.create(business_user=biz, reviewer=cust2, rating=5)
        self.url = reverse('base-info')

    def test_should_return_correct_statistics_200(self):
        """
        Ensures that review count, average rating, business count, 
        and offer count are calculated correctly.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 2)
        self.assertEqual(response.data["average_rating"], 4.5)
        self.assertEqual(response.data["business_profile_count"], 1)
        self.assertEqual(response.data["offer_count"], 1)
