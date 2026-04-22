from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Review
from .serializers import ReviewSerializer
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from auth_app.api.permissions import IsOwnerOrReadOnly


class ReviewListView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [IsAuthenticated]

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.method == 'POST':
            if request.user.type != 'customer':
                raise NotAuthenticated("Only customers can create reviews.")
            biz_id = request.data.get('business_user')
            if Review.objects.filter(reviewer=request.user, business_user_id=biz_id).exists():
                raise PermissionDenied("You can only leave one review per business.")

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]