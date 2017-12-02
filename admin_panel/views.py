# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys ,ast

from django.shortcuts import render
from .FormsHandler import AddProductForm,EditProductForm , AddCategoryForm , AddSurveyForm, AddAdvertiseForm, AddCodeForm
from easybot import models
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from manager import DiscountCodeManager, AdsManager


def adding(request):
    if request.method == 'POST' :
        adding_form = AddProductForm(request.POST, request.FILES)

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
            return render_to_response("adding.html")



    return render_to_response("adding.html", {'cat_data': get_cats_names() })


def showing(request):
    if request.method == 'POST':


        return render_to_response("showing.html",{'product_data':get_product_data()},{'cat_data': get_cats_names() })

    return render_to_response("showing.html", {'product_data':get_product_data() , 'range' : len(get_product_data())},{'cat_data': get_cats_names() })

def edit(request):

    if request.method == 'GET':
        product_id = request.GET['p_id']
        return render_to_response('edit.html',{'p_data':return_product_data(product_id),'cat_data': get_cats_names()})

    if request.method == 'POST':

        edit_form = EditProductForm(request.POST)

        if edit_form.is_valid():
            product_id = request.POST['p_id']
            print(product_id)
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
        print('2')
        return render_to_response("edit.html",{'cat_data': get_cats_names() , 'product':return_product_data(product_id)})

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


def del_naghd(request):
    if request.method == 'GET':
        c_id = request.GET['naghd_id']
        models.Feedback_cat.objects.get(pk=c_id).delete()
        return redirect('/admin-panel/show_naghd_cat/')
    return redirect('/admin-panel/show_naghd_cat/')

def cm_del(request):
    if request.method == 'GET':
        cm_id = request.GET['cm_id']
        models.Comment.objects.get(pk=cm_id).delete()
        return redirect('/admin-panel/enteghadat/')
    return redirect('/admin-panel/enteghadat/')


def add_naghd(request):
    if request.method == 'POST':
        add_feed_cat = AddCategoryForm(request.POST)
        if add_feed_cat.is_valid():
            category_name = add_feed_cat.cleaned_data['category_name']
            try:
                new_category = models.Feedback_cat(fb_name= category_name)
                new_category.save()
            except Exception as e:
                print('error')
                print e
            return redirect("/admin-panel/show_naghd_cat/")
        else:
            print('failed')
            return render_to_response("failed.html")
    return render_to_response('add_feed_cat.html')

def show_naghd_cat(request):
    return render_to_response("feedCat.html" , {'cat_data' : get_feed_cats()})

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
            return redirect('/admin-panel/category/')
        else:
            print('failed')
            return render_to_response("failed.html")
    return render_to_response("add_cat.html")

# Advertise View Handler

def advertise(request):
    ads_object = AdsManager.AdsManager()
    return render_to_response("advertise.html", {'all_ads': ads_object.get_all_ads()})


def add_advertise(request):
    if request.method == 'POST':
        ads_object = AdsManager.AdsManager(ad_data=request.POST, ad_files=request.FILES)
        if ads_object.add_ad():
            return redirect('/admin-panel/advertise/')
        else:
            print "Faild to Add Advertise."
    return render_to_response("add_ad.html")


def del_ad(request):
    if request.method == 'GET':
        ad_id = request.GET['ad_id']
        ads_object = AdsManager.AdsManager(deleted_ad_id=ad_id)
        if ads_object.delete_ad():
            return redirect('/admin-panel/advertise/')
        else:
            print("Error in Deleting Ads")
    return redirect('/admin-panel/advertise/')

# Discount Codes View Handler


def codes(request):
    discount_code_object = DiscountCodeManager.DiscountCodeManager()
    return render_to_response("codes.html", {'all_codes': discount_code_object.get_all_discount_code()})


def add_code(request):
    if request.method == 'POST':
        discount_code_object = DiscountCodeManager.DiscountCodeManager(code_data=request.POST)
        if discount_code_object.add_discount_code():
            return redirect('/admin-panel/add_code/')
    return render_to_response("add_code.html")


def del_code(request):
    if request.method == 'GET':
        code_id = request.GET['code_id']
        discount_code_object = DiscountCodeManager.DiscountCodeManager(deleted_code_id=code_id)
        if discount_code_object.delete_code():
            return redirect('/admin-panel/codes/')
    return redirect('/admin-panel/codes/')

# End Of Discount Code Handler


def survey(request):
    if request.method == 'POST':
        add_survey_form = AddSurveyForm(request.POST)
        if add_survey_form.is_valid():
            survey_title = add_survey_form.cleaned_data['survey_title']
            Q = request.POST.getlist('questions[]') #this list conatins all questions
            questions = []
            for i in range(len(Q)):
                questions.append((Q[i].encode('utf8')))
            try:
                new_survey = models.Surveys(title=survey_title)
                new_survey.save()
                for question in questions:
                    new_question = models.Questions(survey_id=new_survey, text=question)
                    new_question.save()
            except Exception as e:
                print e
            return render_to_response("survey.html")

    return render_to_response("survey.html")

def show_survey(request):
    print "hello!"
    print get_survey_data()
    if request.method == 'POST':
        return render_to_response("show_survey.html" , {'survey_data' : get_survey_data()})
    return render_to_response("show_survey.html", {'survey_data' : get_survey_data()})

def del_survey(request):
    if request.method == 'GET':
        s_id = request.GET['s_id']
        models.Surveys.objects.get(pk=s_id).delete()
        return redirect('/admin-panel/show_survey/')


def del_question(request):
    if request.method == 'GET':
        q_id = request.GET['q_id']
        models.Questions.objects.get(pk=q_id).delete()
        return redirect('/admin-panel/show_survey/')

def enteghadat(request):
    print get_comments()
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


def ed_cat(request):
    if request.method == 'GET':
        cat_id = request.GET['cat_id']
    if request.method == "POST":
        cat_id = request.POST['cat_id']
        new_cat_name = request.POST['new_cat']
        category = models.Category.objects.get(pk=cat_id)
        category.cat_name = new_cat_name
        category.save()
        return redirect('/admin-panel/category/')

    return render_to_response("edit_cat.html", {'cat_data': get_cat_data(cat_id)})

def get_cat_data(cat_id):
    result = models.Category.objects.filter(pk=cat_id)
    cat_data = []
    for cat in result:
        cat_data.append(cat.pk)
        cat_data.append(cat.cat_name)

    return cat_data


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
        update_arrival(order_id=request.GET['o_id'], arrive_state=2)
        return redirect('/admin-panel/orders/')


def inpeyk(request):
    if request.method == "GET":
        update_arrival(order_id=request.GET['o_id'], arrive_state=1)
        return redirect('/admin-panel/orders/')

def success(request):
    return render(request, "admin_panel/blank.html")


def orders(request):
    return render_to_response("orders.html", {'orders_data': get_all_orders()})


def peyk_motori_add(request):
    if request.method == "POST":
        f_name = request.POST['peyk_first_name']
        l_name = request.POST['peyk_last_name']
        phone = request.POST['peyk_phone']
        o_id = request.POST['order_id']
        if add_peyk_motori(f_name=f_name, l_name=l_name, phone=phone, o_id=return_order(o_id=o_id)):
            return redirect('/admin-panel/orders/')
        else:
            print "failed"
    return redirect('/admin-panel/orders/')


def del_order(request):
    if request.method == "GET":
        if delete_order(o_id=request.GET['orderid']):
            return redirect('/admin-panel/orders/')
        else:
            print "failed"
    return redirect('/admin-panel/orders/')




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


def get_feed_cats():
    result = models.Feedback_cat.objects.filter()
    cat_data = []
    all_cat = []
    for cat in result:
        cat_data.append(cat.pk)
        cat_data.append(cat.fb_name)
        all_cat.append(cat_data)
        cat_data = {}

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
        product_data.append(product.image.url)
        product_data.append(product.price)
        all_product.append(product_data)
        product_data = []
    return all_product


def get_survey_data():
    all_surveys = models.Surveys.objects.all()
    all_surveys_data = []
    for survey in all_surveys:
        # add one survey data in dictionary
        # example: {u'questions': [{u'text': u'test1', u'id': 49}, {u'text': u'test2', u'id': 50}], u'title': u'test yeah'}
        survey_data = {}
        # survey contains title
        survey_data['id'] = survey.pk
        survey_data['title'] = survey.title
        all_questions = models.Questions.objects.filter(survey_id=survey)
        all_questions_data_list = []
        for question in all_questions:
            question_data = {}
            question_data['id'] = question.pk
            question_data['text'] = question.text
            all_questions_data_list.append(question_data)
        all_surveys_data.append(survey_data)
        # survey contains questions
        survey_data['questions'] = all_questions_data_list
    return all_surveys_data


def get_comments():
    result = models.Comment.objects.all()
    comments = []
    all_comments = []
    for comment in result:
        comments.append(comment.pk)
        comments.append(return_username_with_telegram_id(comment.telegram_id))
        comments.append(comment.comment)
        comments.append(return_cm_cat_name(comment.comment_cat))
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

def return_product_data(p_id):
    product = models.Product.objects.get(pk=p_id)
    product_dict = {'product_id' : product.pk, 'Name':product.product_name , 'Price': product.price, 'Text': product.text , 'Image' : product.image , 'Number': product.numbers}
    return product_dict

def return_survey_title(s_id):
    survey = models.Surveys.objects.get(pk=s_id)
    survey_title = survey.title
    return survey_title

def update_description(order_id, new_desc):
    try:
        order = models.Order.objects.get(pk=order_id)
        order.additional_info = new_desc
        order.save()
        return 1
    except Exception as e:
        print e
        return 0


def update_arrival(order_id, arrive_state):
    try:
        order = models.Order.objects.get(pk=order_id)
        order.arrived = arrive_state
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

def return_username_with_telegram_id(t_id):
    try:
        customer = models.Customer.objects.get(telegram_id=t_id)
        return customer.username
    except Exception as e:
        return 0


def return_cm_cat_name(c_id):
    try:
        cat_name = models.Feedback_cat.objects.get(pk=c_id)
        return cat_name.fb_name
    except Exception as e:
        return 0


def add_peyk_motori(f_name, l_name, phone, o_id):
    try:
        new_peyk = models.Peyk_motori(order_id=o_id, first_name=f_name, last_name=l_name, phone=phone)
        new_peyk.save()
        return 1
    except Exception as e:
        print e
        return 0


def return_order(o_id):
    try:
        order = models.Order.objects.get(pk=o_id)
        return order
    except Exception as e:
        print e
        return 0


def delete_order(o_id):
    try:
        order = models.Order.objects.get(pk=o_id)
        order.delete()
    except Exception as e:
        print e
        return 0