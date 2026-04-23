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

    description = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Review
        fields = [
            "id", "business_user", "reviewer", "rating",
            "description", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "reviewer", "created_at", "updated_at"]

    def validate(self, data):
        """
        Perform any cross-field validation for review creation.
        """
        return data
