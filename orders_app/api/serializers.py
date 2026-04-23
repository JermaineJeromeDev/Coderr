"""
Serializers for managing orders and mapping offer details to order instances.
"""

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from offers_app.models import OfferDetail
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Handles order creation by extracting data from a specific OfferDetail.
    """
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "customer_user", "business_user", "title", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type",
            "status", "created_at", "updated_at", "offer_detail_id"
        ]
        read_only_fields = [
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type"
        ]

    def create(self, validated_data):
        """
        Creates an order using the current user and data from the 
        linked OfferDetail.
        """
        detail_id = validated_data.pop('offer_detail_id')
        detail = get_object_or_404(OfferDetail, id=detail_id)

        return Order.objects.create(
            customer_user=self.context['request'].user,
            business_user=detail.offer.user,
            title=detail.title,
            revisions=detail.revisions,
            delivery_time_in_days=detail.delivery_time_in_days,
            price=detail.price,
            features=detail.features,
            offer_type=detail.offer_type
        )

    def to_representation(self, instance):
        """
        Ensures price is returned as an integer and removes offer_detail_id.
        """
        rep = super().to_representation(instance)
        if 'price' in rep:
            rep['price'] = int(float(rep['price']))
        return rep