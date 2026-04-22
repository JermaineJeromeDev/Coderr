# 2. Drittanbieter
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from django.db.models import Avg

from offer_app.models import Offer
from reviews_app.models import Review
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token

# 3. Lokale Importe
from .serializers import RegistrationSerializer, UserProfileSerializer


User = get_user_model()


class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id
        }


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class BusinessProfileListView(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(type='business')
    

class CustomerProfileListView(ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(type='customer')
    

class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        business_count = User.objects.filter(type='business').count()
        offer_count = Offer.objects.count()
        return Response({
            "review_count": review_count,
            "average_rating": round(float(avg_rating), 1),
            "business_profile_count": business_count,
            "offer_count": offer_count
        })