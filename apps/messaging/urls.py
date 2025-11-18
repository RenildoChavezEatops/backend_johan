from django.urls import path
from .views import SendWhatsAppView

urlpatterns = [
    path("send/", SendWhatsAppView.as_view()),
]