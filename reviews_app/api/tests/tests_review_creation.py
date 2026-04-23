"""
Tests for creating reviews within the reviews_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from reviews_app.models import Review


User = get_user_model()


class ReviewCreationSuccessTests(APITestCase):
    """
    Test suite for successful review creation.
    """

    def setUp(self):
        """
        Sets up a business user and a customer for review testing.
        """
        self.biz = User.objects.create_user(username="biz", type="business")
        self.cust = User.objects.create_user(username="cust", type="customer")
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('review-list')

    def test_should_create_review_successfully_201(self):
        """
        Ensures a customer can successfully create a review for a business.
        """
        data = {
            "business_user": self.biz.id,
            "rating": 5,
            "description": "Top!"
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)


class ReviewCreationErrorTests(APITestCase):
    """
    Test suite for review creation failure scenarios.
    """

    def setUp(self):
        """
        Sets up business and customer users for error testing.
        """
        self.biz = User.objects.create_user(username="biz", type="business")
        self.cust = User.objects.create_user(username="cust", type="customer")
        self.url = reverse('review-list')

    def test_should_return_401_for_business_user_trying_to_review(self):
        """
        Verifies that business users are not authorized to create reviews.
        """
        biz2 = User.objects.create_user(username="biz2", type="business")
        self.client.force_authenticate(user=biz2)
        data = {"business_user": self.biz.id, "rating": 5}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_duplicate_review(self):
        """
        Ensures that a user can only leave one review per business profile.
        """
        Review.objects.create(
            business_user=self.biz,
            reviewer=self.cust,
            rating=5
        )
        self.client.force_authenticate(user=self.cust)
        data = {"business_user": self.biz.id, "rating": 1, "description": "Too bad."}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_400_when_description_is_missing(self):
        """
        Ensures missing description returns a bad request instead of forbidden.
        """
        self.client.force_authenticate(user=self.cust)
        data = {"business_user": self.biz.id, "rating": 4}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
