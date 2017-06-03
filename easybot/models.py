# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(max_length=20, null=True,unique=True)


class Product(models.Model):
    cat_id = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30, null=True)
    text = models.TextField(null=True)
    image = models.CharField(max_length=60, null=True)
    price = models.IntegerField(null=True)


class Product_comment(models.Model):
    customer_id = models.IntegerField(null=False)
    product_id = models.IntegerField(null=False)
    text_comment = models.TextField(null=True)


class Customer(models.Model):
    telegram_id = models.CharField(max_length=20, null=True,unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    username = models.CharField(max_length=50,unique=True)
    state = models.CharField(max_length=255, default="null")
    current = models.CharField(max_length=255, null=True)


class Comment(models.Model):
    telegram_id = models.CharField(max_length=20)
    comment = models.TextField(null=False)



class Sabad_Kharid(models.Model):
    cus_id = models.ForeignKey(to=Customer,on_delete=models.CASCADE)
    p_id = models.ForeignKey(to=Product,on_delete=models.CASCADE)

    class Meta:
        unique_together= ('cus_id','p_id')

    def __unicode__(self):
        return (unicode(self.cus_id)+'V'+unicode(self.p_id))


class Like_dislike(models.Model):
    telegram_id = models.CharField(max_length=20)
    p_id = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    like = models.BooleanField()

    class Meta:
        unique_together=('telegram_id','p_id')

    def __unicode__(self):
        return (unicode(self.telegram_id)+'V'+unicode(self.p_id))