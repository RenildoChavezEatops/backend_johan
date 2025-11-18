from django.urls import path
from .views import RegisterView, VerifyEmailView, EmailLoginView, CookieTokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", EmailLoginView.as_view()),
    path("verify-email/", VerifyEmailView.as_view()),
    path("refresh/", CookieTokenRefreshView.as_view()),
]
