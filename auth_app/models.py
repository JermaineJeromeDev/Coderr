from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    TYPE_CHOICES = [
        ('business', 'Business'),
        ('customer', 'Customer')
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='customer')
    location = models.CharField(max_length=255, blank=True, default="")
    tel = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=100, blank=True, default="")
    file = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.type})"