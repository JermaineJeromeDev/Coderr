"""
Tests for deleting reviews in the reviews_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from reviews_app.models import Review


User = get_user_model()


class ReviewDeleteSuccessTests(APITestCase):
    """
    Test suite for successful review deletion.
    """

    def setUp(self):
        """
        Sets up the owner, a business user, and a review for deletion.
        """
        self.cust = User.objects.create_user(username="owner", type="customer")
        self.biz = User.objects.create_user(username="biz", type="business")
        self.review = Review.objects.create(
            reviewer=self.cust,
            business_user=self.biz,
            rating=5
        )
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_should_delete_review_successfully_204(self):
        """
        Ensures the owner of a review can successfully delete it.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)


class ReviewDeleteErrorTests(APITestCase):
    """
    Test suite for review deletion failure scenarios (Auth, Permissions, 404).
    """

    def setUp(self):
        """
        Sets up owner, hacker, and a target review for error testing.
        """
        self.owner = User.objects.create_user(username="owner", type="customer")
        self.hacker = User.objects.create_user(username="hacker", type="customer")
        self.biz = User.objects.create_user(username="biz", type="business")
        self.review = Review.objects.create(
            reviewer=self.owner,
            business_user=self.biz,
            rating=5
        )
        self.url = reverse('review-detail', kwargs={'pk': self.review.pk})

    def test_should_return_401_when_not_logged_in(self):
        """
        Ensures unauthenticated users cannot delete reviews.
        """
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_hacker_tries_to_delete(self):
        """
        Verifies that users cannot delete reviews they did not create.
        """
        self.client.force_authenticate(user=self.hacker)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_not_found(self):
        """
        Ensures a 404 error is returned for non-existent review IDs.
        """
        self.client.force_authenticate(user=self.owner)
        url = reverse('review-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)