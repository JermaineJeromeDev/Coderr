"""
URL configuration for the authentication and profile API.
"""

from django.urls import path

from .views import (BaseInfoView, BusinessProfileListView,
                    CustomerProfileListView, LoginView, RegistrationView,
                    UserProfileView)

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