# 2. Drittanbieter
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

# 3. Lokale Importe
from .serializers import RegistrationSerializer


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
