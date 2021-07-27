from django.contrib import admin

from django.contrib import admin
from .models import Message,Message_received
# Register your models here.
admin.site.register(Message)
admin.site.register(Message_received)
