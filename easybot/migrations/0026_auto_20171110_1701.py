# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 17:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0025_auto_20171110_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertise',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads'),
        ),
    ]
