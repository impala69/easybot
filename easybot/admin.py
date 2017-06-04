# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Customer, Product, Category,Sabad_Kharid,Comment, Feedback_cat


admin.site.register(Customer)
admin.site.register(Sabad_Kharid)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Feedback_cat)

# Register your models here.
