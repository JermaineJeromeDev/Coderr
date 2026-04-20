# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class ReviewListSuccessTests(APITestCase):
    """Happy Path: Status 200 und Filterung."""
    def setUp(self):
        self.biz = User.objects.create_user(username="biz", password="p", type="business")
        self.reviewer = User.objects.create_user(username="reviewer", password="p", type="customer")
        self.client.force_authenticate(user=self.reviewer)
        self.url = reverse('review-list')

    def test_should_return_200_for_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewListErrorTests(APITestCase):
    """Unhappy Path: Status 401."""
    def test_should_return_401_when_anonymous(self):
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)