"""
Serializers for managing user reviews and ratings.
"""

# 2. Drittanbieter (Third-party)
from rest_framework import serializers

# 3. Lokale Importe
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model ensuring uniqueness and read-only field safety.
    """

    class Meta:
        model = Review
        fields = [
            "id", "business_user", "reviewer", "rating",
            "description", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, data):
        """
        Prevents users from submitting multiple reviews for the same business.
        """
        reviewer = self.context['request'].user
        business_user = data.get('business_user')

        if Review.objects.filter(
            reviewer=reviewer,
            business_user=business_user
        ).exists():
            raise serializers.ValidationError(
                "You have already reviewed this business."
            )

        return data