"""
Tests for updating order status (PATCH) in the orders_app.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from orders_app.models import Order


User = get_user_model()


class OrderPatchSuccessTests(APITestCase):
    """
    Test suite for successful order status updates.
    """

    def setUp(self):
        """
        Sets up business user, customer, and an order for patching.
        """
        self.biz = User.objects.create_user(
            username="biz",
            password="p",
            type="business"
        )
        self.cust = User.objects.create_user(
            username="cust",
            password="p",
            type="customer"
        )
        self.order = Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            title="T",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_should_update_status_by_business_user_200(self):
        """
        Ensures that a business user can successfully update the order status.
        """
        self.client.force_authenticate(user=self.biz)
        data = {"status": "completed"}
        response = self.client.patch(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")


class OrderPatchErrorTests(APITestCase):
    """
    Test suite for order update failure scenarios.
    """

    def setUp(self):
        """
        Sets up business user, customer, and a target order.
        """
        self.biz = User.objects.create_user(
            username="biz",
            password="p",
            type="business"
        )
        self.cust = User.objects.create_user(
            username="cust",
            password="p",
            type="customer"
        )
        self.order = Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            title="T",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_should_return_400_for_invalid_status(self):
        """
        Verifies that an invalid status value results in a 400 Bad Request.
        """
        self.client.force_authenticate(user=self.biz)
        response = self.client.patch(self.url, {"status": "invalid_status"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_401_when_not_logged_in(self):
        """
        Ensures that unauthenticated users cannot patch orders.
        """
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_customer_tries_to_patch(self):
        """
        Ensures that customers are forbidden from updating order statuses.
        """
        self.client.force_authenticate(user=self.cust)
        response = self.client.patch(self.url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_order_not_found(self):
        """
        Verifies that patching a non-existent order ID returns 404.
        """
        self.client.force_authenticate(user=self.biz)
        invalid_url = reverse('order-detail', kwargs={'pk': 9999})
        response = self.client.patch(invalid_url, {"status": "completed"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)