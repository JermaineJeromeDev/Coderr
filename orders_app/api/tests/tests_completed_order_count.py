# 2. Drittanbieter
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from orders_app.models import Order


User = get_user_model()


class CompletedOrderCountSuccessTests(APITestCase):
    def setUp(self):
        self.biz = User.objects.create_user(username="biz", password="p", type="business")
        self.cust = User.objects.create_user(username="cust", password="p", type="customer")
        for i in range(3):
            Order.objects.create(customer_user=self.cust, business_user=self.biz, status='completed', 
                                title=f"T{i}", revisions=1, delivery_time_in_days=1, price=10)
        Order.objects.create(customer_user=self.cust, business_user=self.biz, status='in_progress', 
                            title="T_run", revisions=1, delivery_time_in_days=1, price=10)
        
        self.client.force_authenticate(user=self.cust)
        self.url = reverse('completed-order-count', kwargs={'business_user_id': self.biz.id})

    def test_should_return_correct_completed_count_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 3)

class CompletedOrderCountErrorTests(APITestCase):
    """Unhappy Paths: 401, 404"""
    def test_should_return_401_when_anonymous(self):
        url = reverse('completed-order-count', kwargs={'business_user_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_404_when_user_not_found(self):
        self.client.force_authenticate(user=User.objects.create_user(username="tmp"))
        url = reverse('completed-order-count', kwargs={'business_user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)