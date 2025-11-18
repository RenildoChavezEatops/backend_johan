from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
