from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.messaging.models import ChatMessage
from apps.messaging.serializers import ChatMessageSerializer


class SendWhatsAppView(APIView):
    def post(self, request):
        to = request.data.get("to")
        message = request.data.get("message")

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            "whatsapp_node",
            {
                "type": "send_whatsapp",
                "to": to,
                "message": message,
            }
        )

        return Response({"status": "sent"})


class ListChatsHistory(ListAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        id_user = self.request.user.id
        return ChatMessage.objects.filter(id_user=id_user)


class ListMessagesByChat(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = ChatMessageSerializer
    def get_queryset(self):
        wa_id = self.request.GET.get("wspId", None)
        if not wa_id:
            return ChatMessage.objects.none()
        return ChatMessage.objects.filter(wa_id=wa_id)

