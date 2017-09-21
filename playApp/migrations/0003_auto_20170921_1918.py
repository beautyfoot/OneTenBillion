# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playApp', '0002_auto_20170921_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='l_circle',
            field=models.IntegerField(choices=[(1, '第一轮'), (2, '第二轮'), (3, '第三轮'), (4, '第四轮'), (5, '第五轮')], verbose_name='比赛轮数'),
        ),
        migrations.AlterField(
            model_name='play',
            name='p_result',
            field=models.SmallIntegerField(choices=[(0, '主队胜'), (1, '客队胜'), (2, '平局')], verbose_name='比赛结果'),
        ),
    ]
