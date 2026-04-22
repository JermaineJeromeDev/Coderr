"""
Tests for listing reviews in the reviews_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class ReviewListSuccessTests(APITestCase):
    """
    Test suite for successful review list retrieval and filtering.
    """

    def setUp(self):
        """
        Sets up business and customer users and authenticates the client.
        """
        self.biz = User.objects.create_user(
            username="biz",
            password="p",
            type="business"
        )
        self.reviewer = User.objects.create_user(
            username="reviewer",
            password="p",
            type="customer"
        )
        self.client.force_authenticate(user=self.reviewer)
        self.url = reverse('review-list')

    def test_should_return_200_for_authenticated_user(self):
        """
        Ensures that authenticated users receive a 200 status when listing reviews.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewListErrorTests(APITestCase):
    """
    Test suite for review list failure scenarios.
    """

    def test_should_return_401_when_anonymous(self):
        """
        Ensures that unauthenticated requests result in a 401 status.
        """
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
