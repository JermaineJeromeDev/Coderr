"""
URL configuration for the offers_app API.
"""

# 1. Standard-Library / Django
from django.urls import path

# 3. Lokale Importe
from .views import (
    OfferDetailSingleView,
    OfferDetailView,
    OfferListView
)


urlpatterns = [
    path(
        'offers/',
        OfferListView.as_view(),
        name='offer-list'
    ),
    path(
        'offers/<int:pk>/',
        OfferDetailView.as_view(),
        name='offer-detail'
    ),
    path(
        'offerdetails/<int:pk>/',
        OfferDetailSingleView.as_view(),
        name='offer-detail-single'
    ),
]
