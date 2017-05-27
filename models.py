# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=20, null=True)

class Product(models.Model):
    cat_id = models.ManyToManyField(Category)
    product_name = models.CharField(max_length=30, null=True)
    text = models.TextField(null=True)
    image = models.CharField(max_length=60, null=True)
    price = models.IntegerField(null=True)


class Customer(models.Model):
    telegram_id = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    username = models.CharField(max_length=50)


class Sabad_Kharid(models.Model):
    cus_id = models.OneToOneField(to=Customer)
    p_id = models.OneToOneField(to=Product)
