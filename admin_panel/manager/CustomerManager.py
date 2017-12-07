from easybot import models
from admin_panel import FormsHandler


class CustomerManager:
    def __init__(self, customer_id=None, telegram_id=None):
        self.customer_id = customer_id
        self.telegram_id = telegram_id

    def return_username_with_telegram_id(self):
        try:
            customer = models.Customer.objects.get(telegram_id=self.telegram_id)
            return customer.username
        except Exception as e:
            print e
            return 0

    def return_username(self):
        try:
            customer = models.Customer.objects.get(pk=self.customer_id)
            return customer.username
        except Exception as e:
            print e
            return 0


