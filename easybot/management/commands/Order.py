from ... import models

class Order:
    def __init__(self , c_id=None , order_time=None, info=None, products=None, order_id=None):
        self.__c_id = c_id
        self.__order_time = order_time
        self.__info = info
        self.__products = products
        self.__order_id = order_id

    def add_card_to_order(self):
        try:
            customer = models.Customer.objects.get(id=self.__c_id)
            row = models.Order(cus_id=customer, additional_info=self.__info, order_time=self.__order_time, arrived=False)
            row.save()
            return (1, row)
        except Exception,err:
            print Exception,err
            return False

    def add_products_to_order(self):
        try:
            print "hiooo"
            for product in self.__products:
                print product.p_id
                row = models.Order_to_product(order_id=self.__order_id, product_id=product.p_id)
                row.save()
            return 1
        except Exception,err:
            print Exception,err
            return 0
