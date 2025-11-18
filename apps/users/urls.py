from django.urls import path
from .views import RegisterView, VerifyEmailView, EmailLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", EmailLoginView.as_view()),
    path("verify-email/", VerifyEmailView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]