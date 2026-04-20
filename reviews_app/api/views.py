from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer


class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']