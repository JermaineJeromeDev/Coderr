# 2. Drittanbieter
from django.db.models import Min
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

# 3. Lokale Importe
from ..models import Offer
from .serializers import OfferSerializer


class OfferPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class OfferListView(ListAPIView):
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

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