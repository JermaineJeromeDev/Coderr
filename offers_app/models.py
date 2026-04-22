"""
Database models for managing service offers and their specific price packages.
"""

# 1. Standard-Library / Django
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Offer(models.Model):
    """
    Represents a general service offer created by a business user.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadata for the Offer model.
        """
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns a string representation of the offer.
        """
        return f"{self.title} by {self.user.username}"


class OfferDetail(models.Model):
    """
    Represents a specific price package (Basic, Standard, Premium) 
    linked to an offer.
    """

    OFFER_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="details"
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=-1)
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    offer_type = models.CharField(
        max_length=10,
        choices=OFFER_TYPES,
        default='basic'
    )

    def __str__(self):
        """
        Returns a string representation of the offer detail.
        """
        return f"Detail for {self.offer.title}: {self.price}€"