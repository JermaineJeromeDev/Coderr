"""
Tests for listing business and customer profiles.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class BusinessProfileListSuccessTests(APITestCase):
    """
    Test suite for successfully retrieving business profiles.
    """

    def setUp(self):
        """
        Creates a business and a customer user for filtering tests.
        """
        self.business_user = User.objects.create_user(
            username="biz_user", password="pass", type="business"
        )
        User.objects.create_user(
            username="cust_user", password="pass", type="customer"
        )
        self.client.force_authenticate(user=self.business_user)
        self.url = reverse('business-profiles')

    def test_should_return_only_business_users(self):
        """
        Verifies that the endpoint returns business profiles 
        and includes the expected user in the paginated results.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check within paginated 'results'
        usernames = [p["username"] for p in response.data['results']]
        self.assertIn("biz_user", usernames)


class BusinessProfileListErrorTests(APITestCase):
    """
    Test suite for business profile listing failures.
    """

    def test_should_return_401_when_anonymous(self):
        """
        Ensures that unauthenticated requests are rejected with 401.
        """
        url = reverse('business-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CustomerProfileListSuccessTests(APITestCase):
    """
    Test suite for successfully retrieving customer profiles.
    """

    def setUp(self):
        """
        Creates a customer and a business user for filtering tests.
        """
        self.customer = User.objects.create_user(
            username="cust_user", password="pass", type="customer"
        )
        User.objects.create_user(
            username="biz_user", password="pass", type="business"
        )
        self.client.force_authenticate(user=self.customer)
        self.url = reverse('customer-profiles')

    def test_should_return_only_customer_users(self):
        """
        Verifies that the endpoint returns customer profiles 
        and includes the expected user in the paginated results.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check within paginated 'results'
        usernames = [p["username"] for p in response.data['results']]
        self.assertIn("cust_user", usernames)


class CustomerProfileListErrorTests(APITestCase):
    """
    Test suite for customer profile listing failures.
    """

    def test_should_return_401_for_business_list_when_anonymous(self):
        """
        Ensures that unauthenticated requests are rejected with 401.
        """
        url = reverse('business-profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
