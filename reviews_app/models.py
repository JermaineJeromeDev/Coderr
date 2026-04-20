from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Review(models.Model):
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.business_user.username}"