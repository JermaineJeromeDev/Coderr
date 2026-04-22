"""
Tests for deleting orders in the orders_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# 3. Lokale Importe
from orders_app.models import Order


User = get_user_model()


class OrderDeleteSuccessTests(APITestCase):
    """
    Test suite for successful order deletion scenarios.
    """

    def setUp(self):
        """
        Sets up a staff user, a common user, and an order for deletion.
        """
        self.staff_user = User.objects.create_user(
            username="admin",
            password="p",
            is_staff=True
        )
        self.common_user = User.objects.create_user(
            username="common",
            password="p"
        )
        self.order = Order.objects.create(
            customer_user=self.common_user,
            business_user=self.staff_user,
            title="T",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_should_delete_order_successfully_as_staff_204(self):
        """
        Ensures that a staff user can successfully delete any order.
        """
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class OrderDeleteErrorTests(APITestCase):
    """
    Test suite for order deletion failure scenarios.
    """

    def setUp(self):
        """
        Sets up a common user, a staff user, and a target order.
        """
        self.common_user = User.objects.create_user(
            username="common",
            password="p"
        )
        self.staff_user = User.objects.create_user(
            username="admin",
            password="p",
            is_staff=True
        )
        self.order = Order.objects.create(
            customer_user=self.common_user,
            business_user=self.staff_user,
            title="T",
            revisions=1,
            delivery_time_in_days=1,
            price=10
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_should_return_401_when_anonymous(self):
        """
        Verifies that unauthenticated requests result in a 401 status.
        """
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_not_staff(self):
        """
        Ensures that non-staff users are forbidden from deleting orders.
        """
        self.client.force_authenticate(user=self.common_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_id_invalid(self):
        """
        Verifies that attempting to delete a non-existent order results in a 404.
        """
        self.client.force_authenticate(user=self.staff_user)
        invalid_url = reverse('order-detail', kwargs={'pk': 9999})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
