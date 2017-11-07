# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-04 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('easybot', '0013_auto_20171021_0747'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, null=True)),
                ('text', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='Peyk_motori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('phone', models.CharField(max_length=20, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='arrived',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='questions',
            name='survey_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easybot.Survey'),
        ),
        migrations.AddField(
            model_name='peyk_motori',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='easybot.Order'),
        ),
    ]
