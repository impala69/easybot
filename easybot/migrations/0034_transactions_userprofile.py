# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-28 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0033_auto_20171214_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id_from_payment', models.IntegerField()),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=30)),
                ('l_name', models.CharField(max_length=30)),
                ('phone_number', models.IntegerField(max_length=50)),
                ('mail', models.EmailField(max_length=50, null=True)),
                ('address', models.TextField(max_length=60, null=True)),
                ('user_type', models.CharField(max_length=30)),
            ],
        ),
    ]
