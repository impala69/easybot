# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
from django.shortcuts import render
from .forms import AddProductForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
sys.path.insert(0, '/E:/final/easybot/easybot/models')
import models
from django.db import IntegrityError
from django.shortcuts import render_to_response

@csrf_protect
def adding(request):
    print(2)
    if request.method == 'POST' :
        print(3)
        print models
        adding_form = AddProductForm(request.POST)
        if adding_form.is_valid():
            product_name = adding_form.cleaned_data['product_name']
            text = adding_form.cleaned_data['product_text']
            image = adding_form.cleaned_data['product_image']
            price = adding_form.cleaned_data['product_price']
            print(text)
            try:
                new_product = models.Product(product_name=product_name,text=text,image=image,price=price)
                new_product.save()
                print new_product

            except:
                pass


            return render_to_response("blank.html")


    return render_to_response("blank.html")

@csrf_protect
def showing(request):
    if request.method == 'POST':
        models_result = models.Product.objects.all()

@csrf_protect
def success(request):
    return render(request, "admin_panel/blank.html")

