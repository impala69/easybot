# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-27 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0036_order_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
