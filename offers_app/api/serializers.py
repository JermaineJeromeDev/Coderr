"""
Serializers for offer management including detailed and short representations.
"""

# 2. Drittanbieter (Third-party)
from rest_framework import serializers

# 3. Lokale Importe
from ..models import Offer, OfferDetail


class OfferDetailDataSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for OfferDetail objects used in POST/PATCH requests.
    """

    id = serializers.IntegerField(required=False)
    price = serializers.IntegerField() 

    class Meta:
        model = OfferDetail
        fields = [
            "id", "title", "revisions", "delivery_time_in_days",
            "price", "features", "offer_type"
        ]


class OfferDetailShortSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for OfferDetail objects used in GET representations.
    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """
        Builds the absolute URI for the offer detail package.
        """
        request = self.context.get('request')
        path = f"/api/offerdetails/{obj.id}/"
        if request:
            return request.build_absolute_uri(path)
        return path


class OfferSerializer(serializers.ModelSerializer):
    """
    Main serializer for Offers, handling nested details and calculated metrics.
    """

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
        """
        Ensures that exactly 3 details are provided during offer creation.
        """
        if self.context['request'].method == 'POST' and len(value) != 3:
            raise serializers.ValidationError("An offer must have exactly 3 details.")
        return value

    def create(self, validated_data):
        """
        Creates an offer along with its nested detail objects.
        """
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        """
        Updates an offer and its associated details based on offer_type.
        """
        details_data = validated_data.pop('details', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data:
            self._update_details(instance, details_data)
        return instance

    def _update_details(self, instance, details_data):
        """
        Helper method to update individual offer details by type.
        """
        for item in details_data:
            offer_type = item.get('offer_type')
            detail_obj = instance.details.filter(offer_type=offer_type).first()
            if detail_obj:
                for attr, value in item.items():
                    setattr(detail_obj, attr, value)
                detail_obj.save()

    def to_representation(self, instance):
        """
        Customizes the output for GET requests to match documentation exactly.
        """
        rep = super().to_representation(instance)
        request = self.context.get('request')
        view = self.context.get('view')

        if request and request.method == 'GET':
            details_qs = instance.details.all()
            rep['details'] = OfferDetailShortSerializer(
                details_qs,
                many=True,
                context={'request': request}
            ).data

            if rep.get('min_price') is not None:
                rep['min_price'] = int(float(rep['min_price']))

            if view and view.__class__.__name__ == 'OfferDetailView':
                rep.pop('user_details', None)

        return rep

    def get_user_details(self, obj):
        """
        Returns basic information about the offer's creator.
        """
        return {
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "username": obj.user.username
        }

    def get_min_price(self, obj):
        """
        Retrieves the annotated min_price from the view's queryset.
        """
        return getattr(obj, 'min_price', 0)

    def get_min_delivery_time(self, obj):
        """
        Retrieves the annotated min_delivery_time from the view's queryset.
        """
        return getattr(obj, 'min_delivery_time', 0)



class OfferCreationSerializer(OfferSerializer):
    """
    Serializer for creating offers with a limited response structure.
    Inherits all validation and creation logic from OfferSerializer.
    """

    class Meta(OfferSerializer.Meta):
        fields = ["id", "title", "image", "description", "details"]
