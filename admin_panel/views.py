# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import AddProductForm
from django.http import HttpResponseRedirect
from easybot import models
from django.db import IntegrityError
from django.shortcuts import render_to_response

def adding(request):
    print models
    if request.method == 'POST' :
        adding_form = AddProductForm(request.POST)
        if adding_form.is_valid():
            product_name = adding_form.cleaned_data['product_name']
            text = adding_form.cleaned_data['product_text']
            image = adding_form.cleaned_data['product_image']
            price = adding_form.cleaned_data['product_price']

            try:
                new_product = Product(product_name=product_name,text=text,image=image,price=price)
                new_product.save()

            except:
                pass


            return render_to_response("templates/charisma-master/blank.html")


    return render_to_response("templates/charisma-master/blank.html")




