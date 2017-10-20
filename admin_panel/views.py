# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

from django.shortcuts import render
from .forms import AddProductForm,EditProductForm , AddCategoryForm
from easybot import models
from django.shortcuts import render_to_response
from django.shortcuts import redirect

def adding(request):
    if request.method == 'POST' :
        adding_form = AddProductForm(request.POST)

        if adding_form.is_valid():
            cat_id = get_cats_names()[0][0]
            cat_id = models.Category.objects.get(pk=cat_id)
            product_name = adding_form.cleaned_data['product_name']
            text = adding_form.cleaned_data['product_text']
            image = adding_form.cleaned_data['product_image']
            price = adding_form.cleaned_data['product_price']

            try:
                new_product = models.Product(cat_id=cat_id,product_name=product_name,text=text,image=image,price=price)
                new_product.save()



            except Exception as e:
                print('error')
                print e


            return render_to_response("showing.html")

        else:
            print('failed')
            return render_to_response("failed.html")



    return render_to_response("adding.html", {'cat_data': get_cats_names() })


def showing(request):
    if request.method == 'POST':


        return render_to_response("showing.html",{'product_data':get_product_data()},{'cat_data': get_cats_names() })

    return render_to_response("showing.html", {'product_data':get_product_data() , 'range' : len(get_product_data())},{'cat_data': get_cats_names() })

def edit(request):

    if request.method == 'GET':
        product_id = request.GET['p_id']
        print(product_id)

        return render_to_response("edit.html",{'cat_data': get_cats_names() , 'product':return_product(product_id)})
    if request.method == 'POST':
        edit_form = EditProductForm(request.POST)

        if edit_form.is_valid():
            print('2')
            cat_id = get_cats_names()[0][0]
            cat_id = models.Category.objects.get(pk=cat_id)
            product_name = edit_form.cleande_data['product_name']
            text = edit_form.cleaned_data['product_text']
            image = edit_form.cleaned_data['product_image']
            price = edit_form.cleaned_data['product_price']
            number = edit_form.cleaned_data['product_number']

            try:
                product_object = models.Product.objects.get(pk=product_id).update(cat_id=cat_id,product_name=product_name,text=text,price=price,image=image,numbers=number)
                product_object.save()
            except Exception as e:
                print('error')
                print e
        return render_to_response('edit.html',{'cat_data': get_cats_names() })
    return render_to_response("edit.html",{'cat_data': get_cats_names() })

def delete(request):
    if request.method == 'GET':
        p_id = request.GET['p_id']
        models.Product.objects.get(pk=p_id).delete()
        return render_to_response("showing.html",{'product_data':get_product_data(),'cat_data': get_cats_names() })
    return render_to_response("showing.html",{'product_data':get_product_data(),'cat_data': get_cats_names() })

def del_cat(request):
    if request.method == 'GET':
        c_id = request.GET['cat_id']
        models.Category.objects.get(pk=c_id).delete()
        return render_to_response('category.html', {'cat_data' : get_cats_names()})
    return render_to_response('category.html', {'cat_data' : get_cats_names()})


def add_cat(request):
    if request.method == 'POST':
        add_cat_form = AddCategoryForm(request.POST)
        if add_cat_form.is_valid():
            category_name = add_cat_form.cleaned_data['category_name']
            try:
                new_category = models.Category(cat_name= category_name)
                new_category.save()
            except Exception as e:
                print('error')
                print e
            return render_to_response("showing.html")
        else:
            print('failed')
            return render_to_response("failed.html")
    return render_to_response("add_cat.html")



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


def editDescription(request):
    if request.method == 'POST':
        order_id = int(request.POST['order_id'])
        new_description = request.POST['edit_description']
        update_description(order_id=order_id, new_desc=new_description)
        return redirect('/admin-panel/orders/')


def deletecomment(request):
    if request.method == 'GET':
        cm_id = int(request.GET['cm_id'])
        delete_comment(cm_id)
        return redirect('/admin-panel/comments/')


def arrived(request):
    if request.method == "GET":
        update_arrival(order_id=request.GET['o_id'])
        return redirect('/admin-panel/orders/')

def success(request):
    return render(request, "admin_panel/blank.html")


def orders(request):
    return render_to_response("orders.html", {'orders_data': get_all_orders()})


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
        comments.append(comment.pk)
        comments.append(return_username(comment.customer_id))
        comments.append(comment.product_id)
        comments.append(comment.text_comment)
        all_comments.append(comments)
        comments = []
    return all_comments

def get_all_orders():
    result = models.Order.objects.all()
    all_orders = []
    for order in result:
        one_order = []
        customer_data = {}
        one_order.append(order.pk)
        customer_id = order.cus_id_id
        customer = models.Customer.objects.get(pk=customer_id)
        customer_data = {'f_name': customer.first_name, "l_name": customer.last_name,"address": customer.address,"phone": customer.phone,"username": customer.username}
        one_order.append(customer_data)
        products = models.Order_to_product.objects.filter(order_id_id=order.pk)
        all_products = []
        for product in products:
            p_data = return_product(product.product_id_id)
            all_products.append(p_data)
        one_order.append(all_products)
        one_order.append(order.additional_info)
        one_order.append(order.order_time)
        one_order.append(order.arrived)
        all_orders.append(one_order)
    return all_orders


def return_product(p_id):
    product = models.Product.objects.get(pk=p_id)
    product_dict = {'product_id': product.pk, 'Name': product.product_name, 'Price':product.price}
    return product_dict


def update_description(order_id, new_desc):
    try:
        order = models.Order.objects.get(pk=order_id)
        order.additional_info = new_desc
        order.save()
        return 1
    except Exception as e:
        print e
        return 0


def update_arrival(order_id):
    try:
        order = models.Order.objects.get(pk=order_id)
        order.arrived = 1
        order.save()
        return 1
    except Exception as e:
        print e
        return 0


def delete_comment(cm_id):
    try:
        comment = models.Product_comment.objects.get(pk=cm_id)
        comment.delete()
        return 1
    except Exception as e:
        return 0


def return_username(cus_id):
    try:
        customer = models.Customer.objects.get(pk=cus_id)
        return customer.username
    except Exception as e:
        return 0