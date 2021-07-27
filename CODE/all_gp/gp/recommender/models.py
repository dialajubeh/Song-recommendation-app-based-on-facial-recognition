from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    emotion = models.CharField(max_length=100000,default="")