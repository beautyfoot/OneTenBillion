# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 19:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubApp', '0001_initial'),
        ('playerApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('name', 'c_name')]),
        ),
    ]
