# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reviews_app.models import Review


User = get_user_model()


class ReviewPatchSuccessTests(APITestCase):
    def setUp(self):
        self.cust = User.objects.create_user(username="cust", type="customer")
        self.biz = User.objects.create_user(username="biz", type="business")
        self.review = Review.objects.create(reviewer=self.cust, business_user=self.biz, rating=3)
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_should_update_review_successfully_200(self):
        data = {"rating": 5, "description": "Update"}
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)


class ReviewPatchErrorTests(APITestCase):
    def setUp(self):
        self.cust = User.objects.create_user(username="cust", type="customer")
        self.hacker = User.objects.create_user(username="hacker", type="customer")
        self.biz = User.objects.create_user(username="biz", type="business")
        self.review = Review.objects.create(reviewer=self.cust, business_user=self.biz, rating=3)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_should_return_401_if_not_logged_in(self):
        response = self.client.patch(self.url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_if_not_owner(self):
        self.client.force_authenticate(user=self.hacker)
        response = self.client.patch(self.url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_review_does_not_exist(self):
        self.client.force_authenticate(user=self.cust)
        url = reverse('review-detail', kwargs={'pk': 9999})
        response = self.client.patch(url, {"rating": 5})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)