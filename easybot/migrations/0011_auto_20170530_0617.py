# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0010_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=20)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='comments',
            name='cus_id',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
    ]
