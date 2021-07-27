from django.contrib import admin

# Register your models here.

from .models import Song,Playlist
# Register your models here.
admin.site.register(Song)
admin.site.register(Playlist)
