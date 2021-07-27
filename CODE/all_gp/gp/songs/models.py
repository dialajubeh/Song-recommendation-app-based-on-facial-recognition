from django.db import models
from django.contrib.auth.models import User
import json,csv
# Create your models here.
import uuid

class Song(models.Model):
    song_name=models.CharField(max_length=200)
    artist=models.CharField(max_length=200)
    songid = models.CharField(max_length=200)
    song_cat= models.CharField(max_length=200)
    def __str__(self):
        return self.song_name


class Playlist(models.Model):
    list_name=models.CharField(max_length=100)
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.CASCADE)
    list = models.ManyToManyField(Song)

    def __str__(self):
        return self.list_name
    def get_list(self):
        return self.list.all()
    def get_name(self):
        return self.list_name