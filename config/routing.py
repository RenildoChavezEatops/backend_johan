from django.urls import path
from apps.messaging.consumers import WhatsAppConsumer

websocket_urlpatterns = [
    path("ws/chat/", WhatsAppConsumer.as_asgi()),
]
