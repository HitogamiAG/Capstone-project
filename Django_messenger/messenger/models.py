from django.db import models
from datetime import datetime


# Create your models here.
class Room(models.Model):
    room = models.CharField(max_length=1000)


class Message(models.Model):
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=1000)
