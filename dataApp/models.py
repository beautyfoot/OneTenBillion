from django.db import models


# Create your models here.


class SpiderUrl(models.Model):
    url = models.CharField(max_length=32, verbose_name="网页", unique=True)
    type = models.CharField(choices=((1, '球员'), (2, '俱乐部'), (3, '比赛')), max_length=5, verbose_name='网页类型')
    flag = models.SmallIntegerField(verbose_name='是否已爬取')
