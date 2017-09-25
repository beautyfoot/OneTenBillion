from django.db import models

# Create your models here.


class League(models.Model):
    '''
    联赛
    '''
    l_name = models.CharField(max_length=32, verbose_name="联赛名")

    def __str__(self):
        return self.l_name

    class Meta:
        verbose_name = "联赛"
        verbose_name_plural = verbose_name


class Club(models.Model):
    '''
    俱乐部
    '''
    c_name = models.CharField(max_length=32, verbose_name="俱乐部名字")
    l_name = models.ForeignKey(League, verbose_name="所属联赛")

    def __str__(self):
        return self.c_name

    class Meta:
        verbose_name = "俱乐部"
        verbose_name_plural = verbose_name



