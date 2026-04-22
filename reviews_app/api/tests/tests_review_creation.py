# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reviews_app.models import Review


User = get_user_model()


class ReviewCreationSuccessTests(APITestCase):
    def setUp(self):
        self.biz = User.objects.create_user(username="biz", type="business")
        self.cust = User.objects.create_user(username="cust", type="customer")
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('review-list')

    def test_should_create_review_successfully_201(self):
        data = {"business_user": self.biz.id, "rating": 5, "description": "Top!"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)


class ReviewCreationErrorTests(APITestCase):
    def setUp(self):
        self.biz = User.objects.create_user(username="biz", type="business")
        self.cust = User.objects.create_user(username="cust", type="customer")
        self.url = reverse('review-list')

    def test_should_return_401_for_business_user_trying_to_review(self):
        biz2 = User.objects.create_user(username="biz2", type="business")
        self.client.force_authenticate(user=biz2)
        response = self.client.post(self.url, {"business_user": self.biz.id, "rating": 5})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_duplicate_review(self):
        Review.objects.create(business_user=self.biz, reviewer=self.cust, rating=5)
        self.client.force_authenticate(user=self.cust)
        data = {"business_user": self.biz.id, "rating": 1}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)