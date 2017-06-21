from django import forms


class NameForm(forms.Form):
    first_name_order = forms.CharField(label='first_name', max_length=30)
    last_name_order = forms.CharField(label='last_name', max_length=30)
    email_order = forms.CharField(label='Email', max_length=50)
    phone_order = forms.CharField(label='Phone', max_length=20)
    bot_name_1 = forms.CharField(label='bot_name_1', max_length=30)
    bot_name_2 = forms.CharField(label='bot_name_2', max_length=30)
    bot_name_3 = forms.CharField(label='bot_name_3', max_length=30)