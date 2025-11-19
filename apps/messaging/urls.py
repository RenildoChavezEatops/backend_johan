from django.urls import path
from .views import SendWhatsAppView, ListChatsHistory, ListMessagesByChat

urlpatterns = [
    path("send/", SendWhatsAppView.as_view()),
    path("get-chats/", ListChatsHistory.as_view()),
    path("get-messages/", ListMessagesByChat.as_view()),
]