from django.db import models
from clubApp.models import Club

# Create your models here.


class PlayPosition(models.Model):
    position = models.CharField(max_length=32, verbose_name="位置")


class Player(models.Model):
    name = models.CharField(max_length=32, verbose_name="名字")
    c_name = models.ForeignKey(Club, verbose_name='俱乐部')
    position = models.ForeignKey(PlayPosition, verbose_name="位置", default=1)



