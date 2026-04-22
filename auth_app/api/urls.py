"""
URL configuration for the authentication and profile API.
"""

# 1. Standard-Library
from django.urls import path

# 3. Lokale Importe
from .views import (
    BaseInfoView,
    RegistrationView,
    LoginView,
    UserProfileView,
    BusinessProfileListView,
    CustomerProfileListView
)


urlpatterns = [
    path(
        'registration/',
        RegistrationView.as_view(),
        name='registration'
    ),
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'profile/<int:pk>/',
        UserProfileView.as_view(),
        name='profile-detail'
    ),
    path(
        'profiles/business/',
        BusinessProfileListView.as_view(),
        name='business-profiles'
    ),
    path(
        'profiles/customer/',
        CustomerProfileListView.as_view(),
        name='customer-profiles'
    ),
    path(
        'base-info/',
        BaseInfoView.as_view(),
        name='base-info'
    ),
]
