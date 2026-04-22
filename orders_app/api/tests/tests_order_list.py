"""
Tests for listing orders in the orders_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class OrderListSuccessTests(APITestCase):
    """
    Test suite for successfully retrieving the order list.
    """

    def setUp(self):
        """
        Sets up various user types for listing tests.
        """
        self.user_customer = User.objects.create_user(
            username="cust",
            password="pass",
            type="customer"
        )
        self.user_business = User.objects.create_user(
            username="biz",
            password="pass",
            type="business"
        )
        self.other_user = User.objects.create_user(
            username="other",
            password="pass"
        )
        self.url = reverse('order-list')

    def test_should_return_200_and_orders_where_user_is_customer(self):
        """
        Verifies that a customer receives a 200 status when accessing their orders.
        """
        self.client.force_authenticate(user=self.user_customer)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderListErrorTests(APITestCase):
    """
    Test suite for order list failure scenarios.
    """

    def test_should_return_401_when_not_logged_in(self):
        """
        Ensures that unauthenticated requests result in a 401 status.
        """
        url = reverse('order-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)