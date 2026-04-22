"""
API views for user registration, authentication, and profile management.
"""

# 2. Drittanbieter (Third-party)
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Avg
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# 3. Lokale Importe
from offers_app.models import Offer
from reviews_app.models import Review
from .permissions import IsOwnerOrReadOnly
from .serializers import RegistrationSerializer, UserProfileSerializer


User = get_user_model()


class RegistrationView(CreateAPIView):
    """
    Handles new user registration and token generation.
    """
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """
    Authenticates users and returns access tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Validates credentials and returns token plus user data.
        """
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                self._format_login_data(user, token),
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Ungültige Anfragedaten."},
            status=status.HTTP_400_BAD_REQUEST
        )

    def _format_login_data(self, user, token):
        """
        Helper to structure the successful login response.
        """
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id
        }


class UserProfileView(RetrieveUpdateAPIView):
    """
    Retrieves or updates individual user profile details.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class BusinessProfileListView(ListAPIView):
    """
    Returns a list of all users with business accounts.
    """
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        """
        Filters the user queryset for business types.
        """
        return User.objects.filter(type='business')


class CustomerProfileListView(ListAPIView):
    """
    Returns a list of all users with customer accounts.
    """
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        """
        Filters the user queryset for customer types.
        """
        return User.objects.filter(type='customer')


class BaseInfoView(APIView):
    """
    Provides platform-wide aggregate statistics.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Calculates and returns total reviews, average rating, 
        business count, and offer count.
        """
        review_count = Review.objects.count()
        avg_res = Review.objects.aggregate(Avg('rating'))['rating__avg']
        avg_rating = round(float(avg_res), 1) if avg_res else 0.0
        business_count = User.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        return Response({
            "review_count": review_count,
            "average_rating": avg_rating,
            "business_profile_count": business_count,
            "offer_count": offer_count
        })