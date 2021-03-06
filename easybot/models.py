# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    cat_name = models.CharField(max_length=20, null=True, unique=True)


class Product(models.Model):
    cat_id = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30, null=True)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='uploads/products', null=True)
    price = models.IntegerField(null=True)
    numbers = models.IntegerField(null=False, default=1)


class Product_comment(models.Model):
    customer_id = models.IntegerField(null=False)
    product_id = models.IntegerField(null=False)
    text_comment = models.TextField(null=True)


class Customer(models.Model):
    telegram_id = models.CharField(max_length=20, null=True, unique=True)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    username = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=255, default="null")
    current = models.CharField(max_length=255, null=True)
    current_cat = models.CharField(max_length=255, null=True)


class Sabad_Kharid(models.Model):
    cus_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    p_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    number = models.IntegerField(null=False, default=1)


    class Meta:
        unique_together = ('cus_id', 'p_id')

    def __unicode__(self):
        return (unicode(self.cus_id) + 'V' + unicode(self.p_id))


class Like_dislike(models.Model):
    telegram_id = models.CharField(max_length=20)
    p_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    like = models.BooleanField()

    class Meta:
        unique_together = ('telegram_id', 'p_id')

    def __unicode__(self):
        return (unicode(self.telegram_id) + 'V' + unicode(self.p_id))


class Feedback_cat(models.Model):
    fb_name = models.CharField(max_length=20, null=False)


class Comment(models.Model):
    telegram_id = models.CharField(max_length=20)
    comment = models.TextField(null=False)
    comment_cat = models.IntegerField(null=True)


class Transactions(models.Model):
    transaction_id_from_payment = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    status = models.IntegerField(null=False)


class Order(models.Model):
    cus_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    additional_info = models.TextField(null=True)
    order_time = models.CharField(max_length=30, null=True)
    arrived = models.IntegerField(default=1)
    transaction = models.ForeignKey(to=Transactions, on_delete=models.CASCADE)

    def __unicode__(self):
        return (unicode(self.id) + 'V' + unicode(self.cus_id))


class Order_to_product(models.Model):
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE)


class Peyk_motori(models.Model):
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)


class Advertise(models.Model):
    title = models.CharField(max_length=300, null=True)
    text = models.TextField(null=True)
    image = models.ImageField(upload_to='uploads/ads', null=True)
    repeat = models.IntegerField(null=False, default=1)

class Surveys(models.Model):
    title = models.CharField(max_length=30 , unique=False)


class Questions(models.Model):
    survey_id = models.ForeignKey(to=Surveys, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)


class DiscountCode(models.Model):
    code_char = models.CharField(max_length=30, null=False, default=None)
    percentage = models.IntegerField(null=False,default=0)


class Answers(models.Model):
    question_id = models.ForeignKey(to=Questions, on_delete=models.CASCADE)
    text = models.TextField(null=False, default=None)



class Ticket(models.Model):
    title = models.CharField(max_length=300, null=True)


class AnswerQuestionTicket(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    order = models.IntegerField(null=True)
    text = models.TextField(null=True)



class UserProfile(models.Model):
    f_name = models.CharField(max_length=30,null=False)
    l_name = models.CharField(max_length=30,null=False)
    phone_number = models.IntegerField(null=False)
    mail = models.EmailField(max_length=50,null=True)
    address = models.TextField(max_length=60,null=True)
    user_type = models.CharField(max_length=30,null=False)
    telegram_id = models.CharField(max_length=30,null=False)

