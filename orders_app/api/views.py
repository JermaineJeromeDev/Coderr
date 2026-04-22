"""
API views for handling orders, status updates, and order statistics.
"""

# 2. Drittanbieter (Third-party)
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied

# 3. Lokale Importe
from ..models import Order
from .serializers import OrderSerializer


User = get_user_model()


class OrderListView(ListCreateAPIView):
    """
    Lists orders for the current user or creates a new order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None 

    def get_queryset(self):
        """
        Filters orders where the user is either customer or business partner.
        """
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_create(self, serializer):
        """
        Ensures only customers can initiate an order.
        """
        if self.request.user.type != 'customer':
            raise PermissionDenied("Only customers can create orders.")
        serializer.save()


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    """
    Detailed view to retrieve, update status, or delete orders.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        """
        Restricts deletion to admin users only.
        """
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Limits access to orders associated with the current user.
        """
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_update(self, serializer):
        """
        Allows only the business user to update the order status.
        """
        if self.request.user != serializer.instance.business_user:
            raise PermissionDenied(
                "Only the business user can update the order status."
            )
        serializer.save()


class OrderCountBaseView(APIView):
    """
    Abstract base view for aggregating order counts.
    """
    permission_classes = [IsAuthenticated]

    def _get_count(self, user_id, status_val):
        """
        Helper to count orders by business user and status.
        """
        user = get_object_or_404(User, id=user_id, type='business')
        return Order.objects.filter(business_user=user, status=status_val).count()


class OrderCountView(OrderCountBaseView):
    """
    Returns the count of currently active (in_progress) orders.
    """

    def get(self, request, business_user_id):
        """
        Calculates and returns the active order count.
        """
        count = self._get_count(business_user_id, 'in_progress')
        return Response({"order_count": count})


class CompletedOrderCountView(OrderCountBaseView):
    """
    Returns the count of finished (completed) orders.
    """

    def get(self, request, business_user_id):
        """
        Calculates and returns the completed order count.
        """
        count = self._get_count(business_user_id, 'completed')
        return Response({"completed_order_count": count})
