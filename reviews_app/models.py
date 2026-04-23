"""
Database models for user reviews and ratings within the Coderr platform.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Review(models.Model):
    """
    Represents a rating and feedback given by a customer to a business user.
    """

    business_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews_received"
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews_given"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Metadata for the Review model.
        """
        unique_together = ('business_user', 'reviewer')
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns a string representation of the review instance.
        """
        return f"Review by {self.reviewer.username} for {self.business_user.username}"