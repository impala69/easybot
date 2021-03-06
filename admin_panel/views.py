# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests, json
from .FormsHandler import AddProductForm, EditProductForm
from easybot import models
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from manager import DiscountCodeManager, AdsManager, SurveyManager, OrderManager, CategoryManager, FeedbackManager, \
    ProductManager, CommentManager, TicketManager, TransactionManager , UserManager



# Product Section

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


def delete_product(request):
    if request.method == 'GET':
        p_id = request.GET['p_id']
        models.Product.objects.get(pk=p_id).delete()
        return redirect("/admin-panel/show_products/")
    return redirect("/admin-panel/show_products/")


# Category Section

def category(request):
    category_object = CategoryManager.CategoryManager()
    return render_to_response("category.html", {'cat_data': category_object.get_all_categories()})


def add_cat(request):
    if request.method == 'POST':
        category_object = CategoryManager.CategoryManager(category_data=request.POST)
        if category_object.add_category():
            return redirect('/admin-panel/category/')
        else:
            print " Failed Adding Category!"
    return render_to_response("add_cat.html")


def del_cat(request):
    if request.method == 'GET':
        c_id = request.GET['cat_id']
        category_object = CategoryManager.CategoryManager(deleted_category_id=c_id)
        if category_object.delete_category():
            return redirect("/admin-panel/category")
        else:
            print "Failed Deleting Category!"
    return redirect("/admin-panel/category/")


def ed_cat(request):
    if request.method == 'GET':
        cat_id = request.GET['cat_id']
        print(cat_id)
        print("koft")
    if request.method == "POST":
        cat_id = request.POST['cat_id']
        print(cat_id)
        new_cat_name = request.POST['new_cat']
        category = models.Category.objects.get(pk=cat_id)
        category.cat_name = new_cat_name
        category.save()
        return redirect('/admin-panel/category/')
    cat_object = CategoryManager.CategoryManager(category_id=cat_id)

    return render_to_response("edit_cat.html", {'cat_data': cat_object.get_category_object()})
#End of Cat Handler

# Feedback Section

def enteghadat(request):
    feedback_object = FeedbackManager.FeedbackManager()
    return render_to_response("enteghadat.html", {'comments': feedback_object.get_all_feedbacks()})


def delete_feedback(request):
    if request.method == 'GET':
        c_id = request.GET['naghd_id']
        feedback_object = FeedbackManager.FeedbackManager(deleted_naghd_id=c_id)
        if feedback_object.delete_feddback_category():
            return redirect('/admin-panel/show_feedback_categories/')
        else:
            print "Failed Deleting Naghd!"
    return redirect('/admin-panel/show_feedback_categories/')


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
            return redirect("/admin-panel/show_feedback_categories/")
        else:
            print('Failed Adding FeedBack Category!')

    return render_to_response('add_feed_cat.html')


def show_feedback_categories(request):
    feedback_object = FeedbackManager.FeedbackManager()
    return render_to_response("show_feedback_categories.html",
                              {'cat_data': feedback_object.get_all_feedback_categories()})


def edit_feedback(request):
    if request.method == 'GET':
        naghd_id = request.GET['naghd_id']
    if request.method == 'POST':
        naghd_id = request.POST['cat_id']
        fb_name = request.POST['new_fb_cat']
        naghd = models.Feedback_cat.objects.get(pk=naghd_id)
        naghd.fb_name = fb_name
        naghd.save()
        return redirect('/admin-panel/show_feedback_categories/')
    feedback_object = FeedbackManager.FeedbackManager(feedback_category_id=naghd_id)
    return render_to_response('edit_feedback.html',{'cat_data': feedback_object.edit_feedback_category()})

# Feedback end

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
 # edit advertisement

def ed_ad(request):
    if request.method == 'GET':
        ad_id = request.GET['ad_id']
    if request.method == 'POST':
        add_id = request.POST['ad_id']
        ad_title = request.POST['ad_name']
        ad_text = request.POST['ad_text']
        ad_image = request.FILES['ad_image']
        ad = models.Advertise.objects.get(pk=add_id)
        ad.title = ad_title
        ad.text = ad_text
        ad.image = ad_image
        ad.save()
        return redirect('/admin-panel/advertise')

    ad_object = AdsManager.AdsManager(edited_ad_id=ad_id)
    return render_to_response('edit_advertise.html', {'ad_data' : ad_object.edit_ad()})
# End of Advertise View Handler


# Discount Codes View Handler


def codes(request):
    discount_code_object = DiscountCodeManager.DiscountCodeManager()
    return render_to_response("codes.html", {'all_codes': discount_code_object.get_all_discount_code()})


def add_code(request):
    if request.method == 'POST':
        discount_code_object = DiscountCodeManager.DiscountCodeManager(code_data=request.POST)
        if discount_code_object.add_discount_code():
            return redirect('/admin-panel/codes/')
    return render_to_response("add_code.html")


def del_code(request):
    if request.method == 'GET':
        code_id = request.GET['code_id']
        discount_code_object = DiscountCodeManager.DiscountCodeManager(deleted_code_id=code_id)
        if discount_code_object.delete_code():
            return redirect('/admin-panel/codes/')
    return redirect('/admin-panel/codes/')

def ed_code(request):
    if request.method == "GET":
        code_id = request.GET['code_id']
    if request.method == "POST":
        code_id = request.POST['code_id']
        code_char = request.POST['code_char']
        percentage = request.POST['percentage']
        dis_code =models.DiscountCode.objects.get(pk=code_id)
        dis_code.code_char = code_char
        dis_code.percentage = percentage
        dis_code.save()
        return redirect('/admin-panel/codes')
    code_object = DiscountCodeManager.DiscountCodeManager(edited_code_id=code_id)
    return render_to_response("edit_code.html",{"code_data":code_object.edit_code()})


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

# Comment Section

def show_product_comments(request):
    comment_object = CommentManager.CommentManager()
    return render_to_response('comments.html', {'p_comment': comment_object.get_all_comments()})


def deletecomment(request):
    if request.method == 'GET':
        cm_id = int(request.GET['cm_id'])
        comment_object = CommentManager.CommentManager(deleted_comment_id=cm_id)
        if comment_object.delete_comment():
            return redirect('/admin-panel/comments/')
        else:
            print "Failed Deleting Product Comment!"


# Order Section

def editDescription(request):
    if request.method == 'POST':
        order_id = int(request.POST['order_id'])
        new_description = request.POST['edit_description']
        order_object = OrderManager.OrderManager(order_id=order_id)
        if order_object.update_description(new_description=new_description):
            return redirect('/admin-panel/orders/')
        else:
            print " Failed Updating Description!"


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


# Ticket Section

def show_tickets(request):
    ticket_object = TicketManager.TicketManager()
    return render_to_response("tickets.html", {'tickets_data': ticket_object.get_all_tickets()})


# Transaction Section

def show_transactions(request):
    transaction_object = TransactionManager.TransactionManager()
    return render_to_response("transactons.html", {'transactions_data': transaction_object.get_all_transactions(), }, )


def payment(request):
    if request.method == "POST":
        if request.POST['status'] == '1':
            r = requests.post("https://pay.ir/payment/verify", data={'api': 'test', 'transId': request.POST['transId']})
            rec_data = json.loads(r.text)
            if rec_data['status'] == 1:
                transaction_object = TransactionManager.TransactionManager(trans_id=request.POST['transId'])
                transaction_object.set_status(state=1)
                return render_to_response("sucess.html", {'transId': request.POST['transId'], 'amount': rec_data['amount']})
            else:
                return render_to_response("fail.html", {'transId': request.POST['transId'], 'amount': rec_data['amount'],
                                                 'error': rec_data['errorMessage']})
        else:
            return render_to_response("fail.html", {'transId': request.POST['transId'],
                                                    'error': request.POST['message']})
def user_profile(request):
    user_data = models.UserProfile.objects.all()
    print(user_data)
    if request.method == "POST":
        user_object = UserManager.UserManager(user_data=request.POST)
        if user_object.edit_user_data():
            print('done')
            return render_to_response('user.html',{'user_data' : user_object.get_user_data()})
    return render_to_response("user.html",{'user_data' : user_data})


