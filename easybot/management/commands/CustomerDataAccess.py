from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class CustomerDataAccess:
    def __init__(self, t_id):
        self.__t_id = t_id

    def return_customer_id(self):
        try:
            customer = models.Customer.objects.get(telegram_id=self.__t_id)
            return customer.id
        except ObjectDoesNotExist:
            customer = None
            return customer

    def add_customer(self, username):
        try:
            entry = models.Customer(telegram_id=self.__t_id, username=username)
            entry.save()
            return True
        except:
            return False


    def check_customer_is(self):
        try:
            customer = get_object_or_404(models.Customer, telegram_id=self.__t_id)
            return 1
        except:
            return 0

    def return_user_state(self):
        try:
            state = models.Customer.objects.get(telegram_id=self.__t_id)
            return state.state
        except ObjectDoesNotExist:
            state = None
            return state

    def set_state(self, state_word):
        try:
            state = models.Customer.objects.get(telegram_id=self.__t_id)
            state.state = state_word
            state.save()
            return True
        except:
            return False

    def unset_state(self):
        try:
            state = models.Customer.objects.get(telegram_id=self.__t_id)
            state.state = ''
            state.save()
            return True
        except:
            return False

    def enter_first_name(self, f_name):
        try:
            customer = models.Customer.objects.get(telegram_id=self.__t_id)
            customer.first_name = f_name
            customer.save()
            return True
        except:
            return False

    def enter_last_name(self, l_name):
        try:
            customer = models.Customer.objects.get(telegram_id=self.__t_id)
            customer.last_name = l_name
            customer.save()
            return True
        except:
            return False

    def enter_address(self, address):
        try:
            customer = models.Customer.objects.get(telegram_id=self.__t_id)
            customer.address = address
            customer.save()
            return True
        except:
            return False

    def enter_phone(self, phone):
        try:
            customer = models.Customer.objects.get(telegram_id=self.__t_id)
            customer.phone = phone
            customer.save()
            return True
        except:
            return False

    def get_current(self):
        try:
            current = models.Customer.objects.get(telegram_id=self.__t_id)
            return current.current
        except ObjectDoesNotExist:
            current = None
            return current

    def set_current(self, current_word):
        try:
            current = models.Customer.objects.get(telegram_id=self.__t_id)
            current.current = current_word
            current.save()
            return True
        except:
            return False

    def get_current_cat(self):
        try:
            current = models.Customer.objects.get(telegram_id=self.__t_id)
            return current.current_cat
        except ObjectDoesNotExist:
            current = None
            return current

    def set_current_cat(self, current_word):
        try:
            current = models.Customer.objects.get(telegram_id=self.__t_id)
            current.current_cat = current_word
            current.save()
            return True
        except:
            return False