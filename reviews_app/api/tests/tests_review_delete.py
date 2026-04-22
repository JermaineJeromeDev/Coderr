# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from reviews_app.models import Review


User = get_user_model()


class ReviewDeleteSuccessTests(APITestCase):
    def setUp(self):
        self.cust = User.objects.create_user(username="owner", type="customer")
        self.biz = User.objects.create_user(username="biz", type="business")
        self.review = Review.objects.create(reviewer=self.cust, business_user=self.biz, rating=5)
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_should_delete_review_successfully_204(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)


class ReviewDeleteErrorTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", type="customer")
        self.hacker = User.objects.create_user(username="hacker", type="customer")
        self.biz = User.objects.create_user(username="biz", type="business")
        self.review = Review.objects.create(reviewer=self.owner, business_user=self.biz, rating=5)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_should_return_401_when_not_logged_in(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_hacker_tries_to_delete(self):
        self.client.force_authenticate(user=self.hacker)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_not_found(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse('review-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)