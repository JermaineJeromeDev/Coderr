# 2. Drittanbieter
from rest_framework import serializers

# 3. Lokale Importe
from ..models import Offer, OfferDetail


class OfferDetailDataSerializer(serializers.ModelSerializer):
    """Vollständige Details für POST/Anzeige nach Erstellung."""
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features"]


class OfferDetailShortSerializer(serializers.ModelSerializer):
    """Kurzform (id, url) für die Liste (GET)."""
    url = serializers.SerializerMethodField()
    class Meta:
        model = OfferDetail
        fields = ["id", "url"]
    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

class OfferSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only=True)
    min_price = serializers.SerializerMethodField(read_only=True)
    min_delivery_time = serializers.SerializerMethodField(read_only=True)
    details = OfferDetailDataSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id", "user", "title", "image", "description", 
            "created_at", "updated_at", "details", 
            "min_price", "min_delivery_time", "user_details"
        ]
        extra_kwargs = {'user': {'read_only': True}}

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("An offer must have exactly 3 details.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def to_representation(self, instance):
        """Spagat: GET liefert Kurzform, POST/Anzeige liefert Langform."""
        rep = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            rep['details'] = OfferDetailShortSerializer(instance.details.all(), many=True).data
        return rep

    def get_user_details(self, obj):
        return {"first_name": obj.user.first_name, "last_name": obj.user.last_name, "username": obj.user.username}

    def get_min_price(self, obj):
        return getattr(obj, 'min_price', 0)

    def get_min_delivery_time(self, obj):
        return getattr(obj, 'min_delivery_time', 0)