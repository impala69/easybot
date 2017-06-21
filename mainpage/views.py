from django.shortcuts import render
from .forms import NameForm
from django.http import HttpResponseRedirect
from models import BotOwner


def index(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        print form.is_valid()
        if form.is_valid():
            first_name = form.cleaned_data['first_name_order']
            last_name = form.cleaned_data['last_name_order']
            email = form.cleaned_data['email_order']
            phone = form.cleaned_data['phone_order']
            bot_name_1 = form.cleaned_data['bot_name_1']
            bot_name_2 = form.cleaned_data['bot_name_2']
            bot_name_3 = form.cleaned_data['bot_name_3']
            new_bot_owner = BotOwner(first_name=first_name, last_name=last_name, email=email, phone=phone, bot_name_1=bot_name_1, bot_name_2=bot_name_2, bot_name_3=bot_name_3)
            new_bot_owner.save()
            return HttpResponseRedirect('/thanks/')

    return render(request, "mainpage/index.html")