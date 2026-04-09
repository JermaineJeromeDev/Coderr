from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = ["user_id", "username", "email", "password", "repeated_password", "type", "token"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('repeated_password')
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key
    

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = [
            "user", "username", "first_name", "last_name", "file",
            "location", "tel", "description", "working_hours",
            "type", "email", "created_at"
        ]
        read_only_fields = ["username", "type", "created_at"]