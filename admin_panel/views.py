# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .FormsHandler import AddProductForm, EditProductForm
from easybot import models
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from manager import DiscountCodeManager, AdsManager, SurveyManager, OrderManager, CategoryManager, FeedbackManager, \
    ProductManager


def add_product(request):
    category_object = CategoryManager.CategoryManager()
    if request.method == 'POST':
        product_object = ProductManager.ProductManager(product_data=request.POST, image_data=request.FILES)
        if product_object.add_product():
            return redirect("/admin-panel/show_products/")
        else:
            return redirect("/admin-panel/add_product/")
    return render_to_response("add_product.html", {'cat_data': category_object.get_all_categories()})


def show_products(request):
    category_object = CategoryManager.CategoryManager()
    product_object = ProductManager.ProductManager()
    return render_to_response("show_products.html", {'product_data': product_object.get_all_products(), },
                              {'cat_data': category_object.get_all_categories()})


def show_product(request):
    if request.method == 'GET':
        product_id = request.GET['p_id']
        product_object = ProductManager.ProductManager(product_id=product_id)
        return render_to_response("show_product.html", {'product_data': product_object.get_product_data()})

def edit(request):
    category_object = CategoryManager.CategoryManager()
    if request.method == 'GET':
        product_id = request.GET['p_id']
        product_object = ProductManager.ProductManager(product_id=product_id)
        return render_to_response('edit.html', {'p_data': product_object.get_product_data(),
                                                'cat_data': category_object.get_all_categories()})

    if request.method == 'POST':
        product_object = ProductManager.ProductManager(product_id=product_id)
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
                product_object = models.Product.objects.get(pk=product_id).update(cat_id=cat_id,
                                                                                  product_name=product_name, text=text,
                                                                                  price=price, image=image,
                                                                                  numbers=number)
                product_object.save()
            except Exception as e:
                print('error')
                print e
        return render_to_response("edit.html",
                                  {'cat_data': get_cats_names(), 'product': product_object.get_product_data()})

    return render_to_response("edit.html", {'cat_data': category_object.get_category_object()})


def delete(request):
    if request.method == 'GET':
        p_id = request.GET['p_id']
        models.Product.objects.get(pk=p_id).delete()
        return redirect("/admin-panel/show_products/")
    return redirect("/admin-panel/show_products/")


def del_cat(request):
    if request.method == 'GET':
        c_id = request.GET['cat_id']
        category_object = CategoryManager.CategoryManager(deleted_category_id=c_id)
        if category_object.delete_category():
            return redirect("/admin-panel/category")
        else:
            print "Failed Deleting Category!"
    return redirect("/admin-panel/category/")


def delete_feedback(request):
    if request.method == 'GET':
        c_id = request.GET['naghd_id']
        naghd_object = FeedbackManager.NaghdManager(deleted_naghd_id=c_id)
        if naghd_object.delete_naghd():
            return redirect('/admin-panel/show_naghd_cat/')
        else:
            print "Failed Deleting Naghd!"
    return redirect('/admin-panel/show_naghd_cat/')


def cm_del(request):
    if request.method == 'GET':
        cm_id = request.GET['cm_id']
        models.Comment.objects.get(pk=cm_id).delete()
        return redirect('/admin-panel/enteghadat/')
    return redirect('/admin-panel/enteghadat/')


def add_feedback_category(request):
    if request.method == 'POST':
        feedback_object = FeedbackManager.FeedbackManager(feedback_category_data=request.POST)
        if feedback_object.add_feedback_category():
            return redirect("/admin-panel/show_naghd_cat/")
        else:
            print('Failed Adding FeedBack Category!')

    return render_to_response('add_feed_cat.html')


def show_feedback_categories(request):
    feedback_object = FeedbackManager.FeedbackManager()
    return render_to_response("feedCat.html", {'cat_data': feedback_object.get_all_feedback_categories()})


def add_cat(request):
    if request.method == 'POST':
        category_object = CategoryManager.CategoryManager(category_data=request.POST)
        if category_object.add_category():
            return redirect('/admin-panel/category/')
        else:
            print " Failed Adding Category!"
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


# End of Advertise View Handler

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

# Survey View Handler


def survey(request):
    if request.method == 'POST':
        survey_object = SurveyManager.SurveyManager(survey_data=request.POST)
        if survey_object.add_survey():
            return redirect('/admin-panel/show_survey/')
        else:
            print "Failed to Add Survey!"
    return render_to_response("survey.html")


def show_survey(request):
    survey_object = SurveyManager.SurveyManager()
    return render_to_response("show_survey.html", {'survey_data': survey_object.get_all_surveys()})


def del_survey(request):
    if request.method == 'GET':
        s_id = request.GET['s_id']
        survey_object = SurveyManager.SurveyManager(deleted_survey_id=s_id)
        if survey_object.delete_survey():
            return redirect('/admin-panel/show_survey/')
        else:
            print "Faild Deleting Survey!"


def del_question(request):
    if request.method == 'GET':
        q_id = request.GET['q_id']
        survey_object = SurveyManager.SurveyManager(deleted_question_id=q_id)
        if survey_object.delete_question():
            return redirect('/admin-panel/show_survey/')
        else:
            print "Failed in Deleting Question!"


# End of Survey View Handler


def enteghadat(request):
    print get_comments()
    if request.method == 'POST':
        return render_to_response("enteghadat.html", {'comments': get_comments()})
    return render_to_response("enteghadat.html", {'comments': get_comments()})


def category(request):
    category_object = CategoryManager.CategoryManager()
    return render_to_response("category.html", {'cat_data': category_object.get_all_categories()})


def comments(request):
    if request.method == 'POST':
        return render_to_response("comments.html", {'p_comment': get_product_comments()})
    return render_to_response('comments.html', {'p_comment': get_product_comments()})


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
        order_id = request.GET['o_id']
        order_object = OrderManager.OrderManager(order_id=order_id, arrival_state=2)
        if order_object.update_arrival():
            return redirect('/admin-panel/orders/')
        else:
            print "Failed Update Arrival in state 2!"


def inpeyk(request):
    if request.method == "GET":
        order_id = request.GET['o_id']
        order_object = OrderManager.OrderManager(order_id=order_id, arrival_state=1)
        if order_object.update_arrival():
            return redirect('/admin-panel/orders/')
        else:
            print "Failed Update Arrival in state 1!"


def orders(request):
    order_object = OrderManager.OrderManager()
    return render_to_response("orders.html", {'orders_data': order_object.get_all_orders()})


def peyk_motori_add(request):
    if request.method == "POST":
        order_object = OrderManager.OrderManager(peyk_data=request.POST)
        if order_object.add_peyk():
            return redirect('/admin-panel/orders/')
        else:
            print "Failed Adding Peyk"
    return redirect('/admin-panel/orders/')


def del_order(request):
    if request.method == "GET":
        o_id = int(request.GET['orderid'])
        order_object = OrderManager.OrderManager(deleted_order_id=o_id)
        if order_object.delete_order():
            return redirect('/admin-panel/orders/')
        else:
            print "failed"
    return redirect('/admin-panel/orders/')


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


def update_description(order_id, new_desc):
    try:
        order = models.Order.objects.get(pk=order_id)
        order.additional_info = new_desc
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
