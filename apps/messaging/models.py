from django.db import models


# Create your models here.

class ChatMessage(models.Model):
    wa_id = models.CharField(max_length=20)
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField()
