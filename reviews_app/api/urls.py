"""
URL configuration for the reviews_app API.
"""

# 1. Standard-Library / Django
from django.urls import path

# 3. Lokale Importe
from .views import ReviewDetailView, ReviewListView


urlpatterns = [
    path(
        'reviews/',
        ReviewListView.as_view(),
        name='review-list'
    ),
    path(
        'reviews/<int:pk>/',
        ReviewDetailView.as_view(),
        name='review-detail'
    ),
]