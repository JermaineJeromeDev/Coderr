# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders_app.models import Order


User = get_user_model()


class OrderDeleteSuccessTests(APITestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(username="admin", password="p", is_staff=True)
        self.common_user = User.objects.create_user(username="common", password="p")
        self.order = Order.objects.create(
            customer_user=self.common_user, business_user=self.staff_user, 
            title="T", revisions=1, delivery_time_in_days=1, price=10
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_should_delete_order_successfully_as_staff_204(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class OrderDeleteErrorTests(APITestCase):
    def setUp(self):
        self.common_user = User.objects.create_user(username="common", password="p")
        self.staff_user = User.objects.create_user(username="admin", password="p", is_staff=True)
        self.order = Order.objects.create(
            customer_user=self.common_user, business_user=self.staff_user, 
            title="T", revisions=1, delivery_time_in_days=1, price=10
        )
        self.url = reverse('order-detail', kwargs={'pk': self.order.pk})

    def test_should_return_401_when_anonymous(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_403_when_not_staff(self):
        """DoD: Ein normaler User (auch wenn es seine Order ist) darf nicht löschen."""
        self.client.force_authenticate(user=self.common_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_return_404_when_id_invalid(self):
        self.client.force_authenticate(user=self.staff_user)
        invalid_url = reverse('order-detail', kwargs={'pk': 9999})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)