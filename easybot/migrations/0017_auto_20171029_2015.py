# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0016_advertise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertise',
            name='image',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]