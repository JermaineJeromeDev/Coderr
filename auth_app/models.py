"""
Database models for the authentication app, including the CustomUser.
"""

# 1. Standard-Library
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model for Coderr platform.
    Supports both business and customer account types with additional metadata.
    """

    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer')
    ]

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='customer'
    )
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Metadata for the CustomUser model.
        """
        ordering = ['id']

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return f"{self.username} ({self.type})"
