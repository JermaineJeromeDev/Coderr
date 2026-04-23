"""
Admin configuration for the reviews_app.
"""

from django.contrib import admin

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