"""
Admin configuration for the offers_app.
"""

from django.contrib import admin

from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """
    Allows editing offer details directly inside the Offer admin page.
    """
    model = OfferDetail
    extra = 3


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    Admin interface for managing offers.
    """
    list_display = ["title", "user", "created_at"]
    inlines = [OfferDetailInline]