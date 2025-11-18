import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone


class WhatsAppConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            await self.accept()
            # Grupo para recibir mensajes desde Node
            await self.channel_layer.group_add("whatsapp_node", self.channel_name)

            # Grupo para enviar mensajes a React
            await self.channel_layer.group_add("frontend_chat", self.channel_name)

            print("Django WebSocket conectado")
        except Exception as e:
            print(f"Error en connect(): {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("whatsapp_node", self.channel_name)
            await self.channel_layer.group_discard("frontend_chat", self.channel_name)
            print(f"WebSocket desconectado: {self.channel_name}")
        except Exception as e:
            print(f"Error en disconnect(): {e}")

    async def receive(self, text_data):
        """
        Node envía mensajes aquí
        Cuando lleguen de whatsapp-web.js
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return await self.safe_send({"error": "JSON inválido"})

        msg_type = data.get("type")
        if msg_type != "whatsapp_message":
            return await self.safe_send({"error": "Tipo de mensaje no soportado"})

        try:
            await self.save_message(data)
        except Exception as e:
            print(f"Error guardando mensaje en BD: {e}")
            return await self.safe_send({"error": "No se pudo guardar el mensaje"})

        try:
            await self.channel_layer.group_send(
                "frontend_chat",
                {
                    "type": "new_message",
                    "message": data,
                },
            )
        except Exception as e:
            print(f"Error reenviando mensaje: {e}")
            await self.safe_send({"error": "No se pudo reenviar el mensaje"})

    async def new_message(self, event):
        try:
            await self.send(text_data=json.dumps(event["message"]))
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

    async def send_whatsapp(self, event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            print(f"Error en send_whatsapp(): {e}")

    async def save_message(self, data):
        from apps.messaging.models import ChatMessage
        try:
            await database_sync_to_async(ChatMessage.objects.create)(
                wa_id=data["from"],
                message=data["message"],
                timestamp=timezone.now()
            )
        except Exception as e:
            print(f"Error en save_message(): {e}")
            raise

    async def safe_send(self, payload: dict):
        try:
            await self.send(json.dumps(payload))
        except Exception:
            pass
