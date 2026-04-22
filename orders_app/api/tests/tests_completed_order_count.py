"""
Tests for counting completed orders for business users.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from orders_app.models import Order


User = get_user_model()


class CompletedOrderCountSuccessTests(APITestCase):
    """
    Test suite for successfully retrieving the completed order count.
    """

    def setUp(self):
        """
        Sets up business user, customer, and multiple orders with mixed statuses.
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

        for i in range(3):
            Order.objects.create(
                customer_user=self.cust,
                business_user=self.biz,
                status='completed',
                title=f"T{i}",
                revisions=1,
                delivery_time_in_days=1,
                price=10
            )

        Order.objects.create(
            customer_user=self.cust,
            business_user=self.biz,
            status='in_progress',
            title="T_run",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )

        self.client.force_authenticate(user=self.cust)
        self.url = reverse(
            'completed-order-count',
            kwargs={'business_user_id': self.biz.id}
        )

    def test_should_return_correct_completed_count_200(self):
        """
        Ensures the endpoint returns only the count of 'completed' orders.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 3)


class CompletedOrderCountErrorTests(APITestCase):
    """
    Test suite for completed order count failure scenarios (401, 404).
    """

    def test_should_return_401_when_anonymous(self):
        """
        Ensures unauthenticated users cannot access the order count.
        """
        url = reverse('completed-order-count', kwargs={'business_user_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_404_when_user_not_found(self):
        """
        Ensures a 404 error is returned for non-existent business user IDs.
        """
        temp_user = User.objects.create_user(username="tmp")
        self.client.force_authenticate(user=temp_user)
        url = reverse('completed-order-count', kwargs={'business_user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
