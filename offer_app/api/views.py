# 2. Drittanbieter
from django.db.models import Min
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError

# 3. Lokale Importe
from ..models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailDataSerializer
from auth_app.api.permissions import IsOwnerOrReadOnly


class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class OfferListView(ListCreateAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.method == 'POST' and request.user.type != 'business':
            self.permission_denied(request, message="Only business users can create offers.")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Offer.objects.annotate(
            min_price=Min('details__price'),
            min_delivery_time=Min('details__delivery_time_in_days')
        ).order_by('-created_at')
        self._validate_ordering()
        return self._apply_custom_filters(queryset)

    def _validate_ordering(self):
        ordering = self.request.query_params.get('ordering')
        if ordering:
            field = ordering.replace('-', '')
            if field not in self.ordering_fields:
                raise ValidationError({"ordering": "Invalid ordering field."})

    def _apply_custom_filters(self, queryset):
        params = self.request.query_params
        try:
            if params.get('creator_id'):
                queryset = queryset.filter(user_id=params.get('creator_id'))
            if params.get('min_price'):
                queryset = queryset.filter(min_price__gte=float(params.get('min_price')))
            if params.get('max_delivery_time'):
                queryset = queryset.filter(min_delivery_time__lte=int(params.get('max_delivery_time')))
        except (ValueError, TypeError):
            raise ValidationError("Invalid filter parameters.")
        return queryset


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Offer.objects.annotate(
        min_price=Min('details__price'),
        min_delivery_time=Min('details__delivery_time_in_days')
    )


class OfferDetailSingleView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailDataSerializer