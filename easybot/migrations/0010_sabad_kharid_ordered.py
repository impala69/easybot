# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-15 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0009_sabad_kharid_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='sabad_kharid',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]