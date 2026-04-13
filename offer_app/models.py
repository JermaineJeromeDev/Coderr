from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Offer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name="offers"
    )
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='offers/', blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.username}"
    

class OfferDetail(models.Model):
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

    def __str__(self):
        return f"Detail for {self.offer.title}: {self.price}€"