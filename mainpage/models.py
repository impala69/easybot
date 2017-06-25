# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class BotOwner(models.Model):
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    transaction_number = models.CharField(max_length=12, unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True, null=True)
    bot_name_1 = models.CharField(max_length=30, null=True)
    bot_name_2 = models.CharField(max_length=30, null=True)
    bot_name_3 = models.CharField(max_length=30, null=True)

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    message = models.TextField()