# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from django.shortcuts import render
from .forms import AddProductForm,EditProductForm
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


            return render_to_response("adding.html", {'cat_data': get_cats_names() })

        else:
            print('failed')
            return render_to_response("failed.html", {'cat_data': get_cats_names() })



    return render_to_response("adding.html", {'cat_data': get_cats_names() })


def showing(request):
    if request.method == 'POST':
        '''edit_form = EditProductForm(request.POST)
        print(get_product_data()[0][0])
        if edit_form.is_valid():
            product_id = '''

        return render_to_response("showing.html", {'product_data':get_product_data()})
    print(get_product_data()[0])
    return render_to_response("showing.html", {'product_data':get_product_data() , 'range' : len(get_product_data())})


def enteghadat(request):
    if request.method == 'POST':
        return render_to_response("enteghadat.html" , {'comments': get_comments()})
    return render_to_response("enteghadat.html" , {'comments' : get_comments()})


def category(request):
    if request.method == 'POST':
        return render_to_response("category.html" , {'cat_data' : get_cats_names()})
    return render_to_response("category.html" , {'cat_data' : get_cats_names()})

def comments(request):
    if request.method == 'POST':
        return render_to_response("comments.html" , {'p_comment' : get_product_comments()})
    return render_to_response('comments.html' , {'p_comment' : get_product_comments()})


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

def get_product_data():
   result = models.Product.objects.all()
   product_data = []
   all_product = []
   for product in result:
       product_data.append(product.pk)
       product_data.append(product.cat_id)
       product_data.append(product.product_name)
       product_data.append(product.text)
       product_data.append(product.image)
       product_data.append(product.price)
       all_product.append(product_data)
       product_data = []

   return all_product

def get_comments():
    result = models.Comment.objects.all()
    comments = []
    all_comments = []
    for comment in result:
        comments.append(comment.telegram_id)
        comments.append(comment.comment)
        comments.append(comment.comment_cat)
        all_comments.append(comments)
        comments = []
    return all_comments

def get_product_comments():
    result = models.Product_comment.objects.all()
    comments = []
    all_comments = []
    for comment in result:
        comments.append(comment.customer_id)
        comments.append(comment.product_id)
        comments.append(comment.text_comment)
        all_comments.append(comments)
        comments = []
    return all_comments