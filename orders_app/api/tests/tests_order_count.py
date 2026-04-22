"""
Tests for counting in-progress orders for business users.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from orders_app.models import Order


User = get_user_model()


class OrderCountSuccessTests(APITestCase):
    """
    Test suite for successfully retrieving the in-progress order count.
    """

    def setUp(self):
        """
        Sets up business user, customer, and orders with different statuses.
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

        Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            status='in_progress',
            title="T1",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )
        Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            status='in_progress',
            title="T2",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )
        Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            status='completed',
            title="T3",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )

        self.client.force_authenticate(user=self.cust)
        self.url = reverse(
            'order-count',
            kwargs={'business_user_id': self.biz.id}
        )

    def test_should_return_correct_order_count_200(self):
        """
        Ensures the endpoint returns the correct count of 'in_progress' orders.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_count"], 2)


class OrderCountErrorTests(APITestCase):
    """
    Test suite for order count failure scenarios (401, 404).
    """

    def test_should_return_401_when_anonymous(self):
        """
        Ensures unauthenticated users cannot access the order count.
        """
        url = reverse('order-count', kwargs={'business_user_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_404_when_user_is_not_business(self):
        """
        Ensures a 404 error is returned if the target ID is not a business user.
        """
        cust = User.objects.create_user(username="only_cust", type="customer")
        self.client.force_authenticate(user=cust)
        url = reverse('order-count', kwargs={'business_user_id': cust.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
