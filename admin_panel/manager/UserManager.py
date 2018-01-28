from easybot import models
from admin_panel import FormsHandler

class UserManager:
    def __init__(self , user_data=None):
        self.user_data = user_data

#Add admins to Database
    def edit_user_data(self):
        add_user_form = FormsHandler.AddUserProfile(self.user_data)
        admin_number = len(models.UserProfile.objects.all())
        print(admin_number)
        if admin_number == 0 :
            if add_user_form.is_valid():
                f_name = add_user_form.cleaned_data['user_first_name']
                l_name = add_user_form.cleaned_data['user_last_name']
                phone = add_user_form.cleaned_data['user_phone']
                mail = add_user_form.cleaned_data['user_mail']
                address = add_user_form.cleaned_data['user_address']
                user_type = add_user_form.cleaned_data['user_type']
                telegram_id = add_user_form.cleaned_data['user_telegram_id']
                try:
                    new = models.UserProfile(f_name = f_name, l_name = l_name, phone_number =phone, mail = mail,address = address, user_type = user_type,telegram_id = telegram_id)
                    new.save()
                    return 1
                except Exception as e:
                    print e
                    return 0

        else:

            if add_user_form.is_valid():
                f_name = add_user_form.cleaned_data['user_first_name']
                l_name = add_user_form.cleaned_data['user_last_name']
                phone = add_user_form.cleaned_data['user_phone']
                mail = add_user_form.cleaned_data['user_mail']
                address = add_user_form.cleaned_data['user_address']
                user_type = add_user_form.cleaned_data['user_type']
                telegram_id = add_user_form.cleaned_data['user_telegram_id']
                try:
                    user = models.UserProfile.objects.get(pk=1)
                    user.f_name = f_name
                    user.l_name = l_name
                    user.phone_number = phone
                    user.mail = mail
                    user.address = address
                    user.user_type = user_type
                    user.telegram_id = telegram_id
                    user.save()
                    return 1
                except Exception as e:
                    print e
                    return 0
            else:
                return 0

#Get all admins data
    def get_user_data(self):
        result = models.UserProfile.objects.all()
        users = []
        for user in result:
            user_dict = {}
            user_dict['id'] = user.pk
            user_dict['f_name'] = user.f_name
            user_dict['l_name'] = user.l_name
            user_dict['phone_number'] = user.phone_number
            user_dict['address'] = user.address
            user_dict['mail'] = user.mail
            user_dict['user_type'] = user.user_type
            users.append(user_dict)

        return users

