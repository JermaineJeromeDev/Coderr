"""
API views for handling service reviews and detailed review management.
"""

# 2. Drittanbieter (Third-party)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

# 3. Lokale Importe
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

    def check_permissions(self, request):
        """
        Validates user type and prevents duplicate reviews for the same business.
        """
        super().check_permissions(request)
        if request.method == 'POST':
            if request.user.type != 'customer':
                raise NotAuthenticated("Only customers can create reviews.")

            biz_id = request.data.get('business_user')
            exists = Review.objects.filter(
                reviewer=request.user,
                business_user_id=biz_id
            ).exists()

            if exists:
                raise PermissionDenied("You can only leave one review per business.")

    def perform_create(self, serializer):
        """
        Assigns the current authenticated user as the reviewer.
        """
        serializer.save(reviewer=self.request.user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    Handles retrieval, partial updates, and deletion of specific reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]