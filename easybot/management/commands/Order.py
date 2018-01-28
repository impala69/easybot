from ... import models

class Order:
    def __init__(self , c_id=None , order_time=None, info=None, products=None, order_id=None, transaction=None, customer=None):
        self.__c_id = c_id
        self.__order_time = order_time
        self.__info = info
        self.__products = products
        self.__order_id = order_id
        self.transaction = transaction
        self.customer = customer

    def add_card_to_order(self):
        try:
            customer = models.Customer.objects.get(id=self.__c_id)
            row = models.Order(cus_id=customer, additional_info=self.__info, order_time=self.__order_time, arrived=False, transaction=self.transaction)
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

    def return_transaction_with_customer(self):
        try:
            order = models.Order.objects.filter(cus_id_id=self.customer)
            return order
        except Exception as e:
            print e
            return 0

    def get_all_orders(self):
        result = models.Order.objects.all()
        all_orders = []
        for order in result:
            all_orders.append(order.pk)
        return all_orders

    def get_order(self):
        order = models.Order.objects.get(pk=self.__order_id)
        one_order = []
        one_order.append(order.pk)
        customer_id = order.cus_id_id
        customer = models.Customer.objects.get(pk=customer_id)
        customer_data = {'f_name': customer.first_name, "l_name": customer.last_name, "address": customer.address,
                         "phone": customer.phone, "username": customer.username}
        one_order.append(customer_data)
        products = models.Order_to_product.objects.filter(order_id_id=order.pk)
        all_products = []
        for product in products:
            product = models.Product.objects.get(pk=product.product_id_id)
            product_dict = {'product_id': product.pk, 'Name': product.product_name, 'Price': product.price}
            all_products.append(product_dict)
        one_order.append(all_products)
        one_order.append(order.additional_info)
        one_order.append(order.order_time)
        one_order.append(order.arrived)
        return one_order
