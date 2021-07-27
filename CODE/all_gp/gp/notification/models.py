from django.db import models
from django.contrib.auth.models import User
from songs.models import Song
import time
from django.contrib.auth import get_user_model

class Message(models.Model):
     sender_msg = models.ForeignKey(User, on_delete=models.CASCADE)
     receiver_msg = models.TextField(default="")
     message_file = models.ForeignKey(Song, on_delete=models.CASCADE)
     timestamp = models.DateTimeField(auto_now_add=True)

class Message_received(models.Model):
     sender = models.TextField(default="")
     receiver = models.ForeignKey(User, on_delete=models.CASCADE)
     message_file = models.ForeignKey(Song, on_delete=models.CASCADE)
     timestamp = models.DateTimeField(auto_now_add=True)
