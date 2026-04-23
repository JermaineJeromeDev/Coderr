"""
API views for handling service reviews and detailed review management.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from auth_app.api.permissions import IsOwnerOrReadOnly
from ..models import Review
from .serializers import ReviewSerializer


class ReviewListView(ListCreateAPIView):
    """
    Lists all reviews with filtering or creates a new review for a business.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def check_permissions(self, request):
        """
        Validates user type for review creation.
        """
        super().check_permissions(request)
        if request.method == 'POST' and request.user.type != 'customer':
            raise PermissionDenied("Only customers can create reviews.")

    def perform_create(self, serializer):
        """
        Prevent duplicate reviews and assign the current user as reviewer.
        """
        biz_id = serializer.validated_data.get('business_user').id
        exists = Review.objects.filter(
            reviewer=self.request.user,
            business_user_id=biz_id
        ).exists()

        if exists:
            raise PermissionDenied("You can only leave one review per business.")

        serializer.save(reviewer=self.request.user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    Handles retrieval, partial updates, and deletion of specific reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]