from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from .serializers import RegisterSerializer, EmailTokenObtainPairSerializer
from .models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        token = default_token_generator.make_token(user)
        uid = user.pk

        verification_link = f"http://localhost:8001/api/users/verify-email/?uid={uid}&token={token}"

        send_mail(
            "Verifica tu correo",
            f"Hola {user.username}, haz click aquí para verificar tu cuenta:\n{verification_link}",
            "johan.jara@test",
            [user.email],
        )


class VerifyEmailView(APIView):
    def get(self, request):
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Correo verificado correctamente"})

        return Response({"error": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)


class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        access = data.get("access")
        refresh = data.get("refresh")

        response.data = {"detail": "login successful"}

        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 4,  # 4 min
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,  # 7 días
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")

        if refresh is None:
            return Response({"detail": "No refresh token"}, status=401)

        request.data["refresh"] = refresh
        response = super().post(request, *args, **kwargs)

        access = response.data.get("access")
        response.data = {"detail": "token refreshed"}

        response.set_cookie(
            "access_token",
            access,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 30,
        )

        return response
