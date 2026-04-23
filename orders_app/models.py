"""
Database models for managing customer orders and their current lifecycle status.
"""

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    """
    Represents a contractual agreement between a customer and a business user.
    Stores a snapshot of the offer details at the time of purchase.
    """

    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_orders"
    )
    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="business_orders"
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadata for the Order model.
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns a string representation of the order instance.
        """
        return f"Order {self.id}: {self.title}"