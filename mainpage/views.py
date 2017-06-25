# -*- coding: utf-8 -*-

from django.shortcuts import render
from .forms import OrderForm, ContactForm
from django.http import HttpResponseRedirect
from models import BotOwner, Contact
from django.db import IntegrityError
from django.shortcuts import render_to_response


def index(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            first_name = order_form.cleaned_data['first_name_order']
            last_name = order_form.cleaned_data['last_name_order']
            email = order_form.cleaned_data['email_order']
            phone = order_form.cleaned_data['phone_order']
            bot_name_1 = order_form.cleaned_data['bot_name_1']
            bot_name_2 = order_form.cleaned_data['bot_name_2']
            bot_name_3 = order_form.cleaned_data['bot_name_3']

            try:
                new_bot_owner = BotOwner(first_name=first_name, last_name=last_name, email=email, phone=phone, bot_name_1=bot_name_1, bot_name_2=bot_name_2, bot_name_3=bot_name_3)
                new_bot_owner.save()
                trans_id = hash_id(new_bot_owner.pk, new_bot_owner.phone)
                bot_owner = BotOwner.objects.get(pk=new_bot_owner.pk)
                bot_owner.transaction_number = trans_id
                bot_owner.save()
                return success(request, trans_id)

            except IntegrityError as e:
                error_msg = e[1]
                if "Duplicate entry" in error_msg:
                    if "email" in error_msg:
                        message = "ایمیل وارد شده تکراری می باشد".decode('utf-8')
                        submit_form_var = "failed_email"
                    elif "phone" in error_msg:
                        message = "شماره تلفن وارد شده تکراری می باشد".decode('utf-8')
                        submit_form_var = "failed_phone"
                print e

            return render_to_response("mainpage/index.html", {"message": message, "submit_form": submit_form_var})





    return render(request, "mainpage/index.html", {"submit_form": "false"})

def success(request, trans_id):
    return render(request, "mainpage/success.html", {'trans_id': trans_id})

def contact(request):
    if request.method == 'POST':

        contact_form = ContactForm(request.POST)
        print contact_form
        if contact_form.is_valid():
            print 3
            first_name = contact_form.cleaned_data['first_name_contact']
            last_name = contact_form.cleaned_data['last_name_contact']
            email = contact_form.cleaned_data['email_contact']
            message = contact_form.cleaned_data['message_contact']

            try:
                print 1
                new_contact = Contact(first_name=first_name, last_name=last_name, email=email, message=message)
                new_contact.save()
                return render_to_response("mainpage/successcontact.html")

            except IntegrityError as e:
                error_msg = e[1]
                print e

    return HttpResponseRedirect("/")



def hash_id(id, phone):
    return int(id) * 256 + int(phone)
