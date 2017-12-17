# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-10 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0021_merge_20171110_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertise',
            name='repeat',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='advertise',
            name='image',
            field=models.CharField(max_length=255, null=True),
        ),
    ]