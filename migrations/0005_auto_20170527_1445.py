# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0004_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
