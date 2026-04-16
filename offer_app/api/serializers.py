# 2. Drittanbieter
from rest_framework import serializers

# 3. Lokale Importe
from ..models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()


    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description", 
            "created_at", "updated_at", "details", 
            "min_price", "min_delivery_time", "user_details"
        ]

    def get_user_details(self, obj):
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def get_min_price(self, obj):
        return getattr(obj, 'min_price', 0)

    def get_min_delivery_time(self, obj):
        return getattr(obj, 'min_delivery_time', 0)