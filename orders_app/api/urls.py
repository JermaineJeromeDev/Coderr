from django.urls import path
from .views import OrderCountView, OrderListView, OrderDetailView


urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order-count/<int:business_user_id>/', OrderCountView.as_view(), name='order-count'),
]