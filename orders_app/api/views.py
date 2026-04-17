# 2. Drittanbieter
from django.db.models import Q
from django.db.models import Min
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied 

# 3. Lokale Importe
from ..models import Order
from .serializers import OrderSerializer


class OrderListView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_create(self, serializer):
        if self.request.user.type != 'customer':
            raise PermissionDenied("Only customers can create orders.")
        serializer.save()


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.business_user:
            raise PermissionDenied("Only the business user can update the order status.")
        serializer.save()