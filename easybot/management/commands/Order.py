from ... import models

class Order:
    def __init__(self , c_id , order_time, info):
        self.__c_id = c_id
        self.__order_time = order_time
        self.__info = info

    def add_card_to_order(self):
        try:
            customer = models.Customer.objects.get(id=self.__c_id)
            row = models.Order(cus_id=customer, additional_info=self.__info, order_time=self.__order_time, arrived=False)
            row.save()
            return True
        except Exception,err:
            print Exception,err
            return False
