# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-27 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0035_transactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transaction',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='easybot.Transactions'),
            preserve_default=False,
        ),
    ]
