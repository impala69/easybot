# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from suit.widgets import EnclosedInput,NumberInput

from .models import Customer, Product, Category,Sabad_Kharid,Comment, Feedback_cat, Advertise


class ProductForm(ModelForm):
    class Meta:
        widgets = {

            'product_name': EnclosedInput(prepend='icon-user'),


            # By icons
            'text': EnclosedInput(prepend='icon-envelope'),
            'image': EnclosedInput(prepend = 'icon-picture'),

            # You can also use prepended and appended together
            'price': EnclosedInput(prepend='$', append='.00'),

        }
class ProductAdmin(ModelAdmin):
    form = ProductForm

class Product_CommentForm(ModelForm):
    class Meta:
        widgets = {
            'text_comment' : EnclosedInput(prepend='icon-comment')
        }
class Product_CommentAdmin(ModelAdmin):
    form = Product_CommentForm

class CustomerForm(ModelForm):
    class Meta:
        widgets = {
            'telegram_id' : NumberInput(attrs={'class': 'input-mini'}),
            'first_name' : EnclosedInput(prepend='icon-user'),
            'last_name' : EnclosedInput(prepend='icon-user'),
            'address' : EnclosedInput(prepend='icon-map-marker'),
            'phone' : EnclosedInput(prepend='icon-phone'),
            'username' : EnclosedInput(prepend='icon-user'),
            'state' : EnclosedInput(prepend='icon-exclamation-sign'),
            'current' : EnclosedInput(prepend='icon-exclamation-sign'),


        }
class CustomerAdmin(ModelAdmin):
    form = CustomerForm

admin.site.register(Customer , CustomerAdmin)
admin.site.register(Sabad_Kharid)
admin.site.register(Product ,ProductAdmin)
admin.site.register(Category)
admin.site.register(Comment , Product_CommentAdmin)
admin.site.register(Feedback_cat)
admin.site.register(Advertise)

# Register your models here.
