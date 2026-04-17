# 2. Drittanbieter
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from offer_app.models import OfferDetail

# 3. Lokale Importe
from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "customer_user", "business_user", "title", "revisions", 
            "delivery_time_in_days", "price", "features", "offer_type", 
            "status", "created_at", "updated_at", "offer_detail_id"
        ]
        read_only_fields = [
            "customer_user", "business_user", "title", "revisions", 
            "delivery_time_in_days", "price", "features", "offer_type", "status"]

    def create(self, validated_data):
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