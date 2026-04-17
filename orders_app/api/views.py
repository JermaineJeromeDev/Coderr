# 2. Drittanbieter
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

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
        serializer.save()

