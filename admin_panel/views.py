# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from django.shortcuts import render
from .forms import AddProductForm
from easybot import models
from django.shortcuts import render_to_response

def adding(request):
    if request.method == 'POST' :
        adding_form = AddProductForm(request.POST)

        print(get_cats_names()[0][0])
        if adding_form.is_valid():
            cat_id = get_cats_names()[0][0]
            cat_id = models.Category.objects.get(pk=cat_id)
            product_name = adding_form.cleaned_data['product_name']
            text = adding_form.cleaned_data['product_text']
            image = adding_form.cleaned_data['product_image']
            price = adding_form.cleaned_data['product_price']

            try:
                new_product = models.Product(cat_id=cat_id,product_name=product_name,text=text,image=image,price=price)
                print new_product.text
                new_product.save()
                print new_product.text


            except Exception as e:
                print('error')
                print e


            return render_to_response("blank.html")

        else:
            print('failed')
            return render_to_response("failed.html")



    return render_to_response("blank.html", {'cat_data': get_cats_names() })


def showing(request):
    if request.method == 'POST':
        models_result = models.Product.objects.all()


def success(request):
    return render(request, "admin_panel/blank.html")


def get_cats_names():
    result = models.Category.objects.filter()
    cat_data = []
    all_cat = []
    for cat in result:
        cat_data.append(cat.pk)
        cat_data.append(cat.cat_name)
        all_cat.append(cat_data)
        cat_data = []

    return all_cat

