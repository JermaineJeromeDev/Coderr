"""
Admin configuration for the reviews_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib import admin

# 3. Lokale Importe
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for managing customer reviews.
    """

    list_display = [
        "business_user",
        "reviewer",
        "rating",
        "created_at"
    ]