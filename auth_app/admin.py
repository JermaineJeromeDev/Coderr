"""
Admin configuration for the auth_app.
"""

# 2. Drittanbieter (Third-party)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# 3. Lokale Importe
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom user admin to handle additional fields like 'type'.
    """
    model = CustomUser
    list_display = ["username", "email", "type", "is_staff"]
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("type", "location", "tel", "description", "working_hours", "file")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("type",)}),
    )