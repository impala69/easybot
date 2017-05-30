# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import Customer, Product, Category,Sabad_Kharid,Comment


admin.site.register(Customer)
admin.site.register(Sabad_Kharid)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)

# Register your models here.
