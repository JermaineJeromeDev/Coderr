"""
Admin configuration for the orders_app.
"""

from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for managing customer orders.
    """

    list_display = [
        "id",
        "customer_user",
        "business_user",
        "status",
        "created_at"
    ]
    list_filter = ["status"]