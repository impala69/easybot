from easybot import models
from admin_panel import FormsHandler


class OrderManager:
    def __init__(self, peyk_data=None, deleted_order_id=None, order_id=None, arrival_state=None):
        self.deleted_order_id = deleted_order_id
        self.peyk_data = peyk_data
        self.order_id = order_id
        self.arrival_state = arrival_state

    def get_all_orders(self):
        result = models.Order.objects.all()
        all_orders = []
        for order in result:
            one_order = []
            customer_data = {}
            one_order.append(order.pk)
            customer_id = order.cus_id_id
            customer = models.Customer.objects.get(pk=customer_id)
            customer_data = {'f_name': customer.first_name, "l_name": customer.last_name, "address": customer.address,
                             "phone": customer.phone, "username": customer.username}
            one_order.append(customer_data)
            products = models.Order_to_product.objects.filter(order_id_id=order.pk)
            all_products = []
            for product in products:
                p_data = return_product(product.product_id_id)
                all_products.append(p_data)
            one_order.append(all_products)
            one_order.append(order.additional_info)
            one_order.append(order.order_time)
            one_order.append(order.arrived)
            all_orders.append(one_order)
        return all_orders

    def delete_order(self):
        try:
            models.Order.objects.get(pk=self.deleted_order_id).delete()
            return 1
        except Exception as e:
            print e
            return 0

    def add_peyk(self):
        add_peyk_form = FormsHandler.AddPeykForm(self.peyk_data)
        if add_peyk_form.is_valid():
            o_id = add_peyk_form.cleaned_data['order_id']
            f_name = add_peyk_form.cleaned_data['peyk_first_name']
            l_name = add_peyk_form.cleaned_data['peyk_last_name']
            phone = add_peyk_form.cleaned_data['peyk_phone']
            try:
                new_peyk = models.Peyk_motori(order_id=self.get_order_object(), first_name=f_name,
                                              last_name=l_name, phone=phone)
                new_peyk.save()
                return 1
            except Exception as e:
                print e
                return 0

    def get_order_object(self):
        return models.Order.objects.get(pk=self.order_id)

    def update_arrival(self):
        try:
            order = models.Order.objects.get(pk=self.order_id)
            order.arrived = self.arrival_state
            order.save()
            return 1
        except Exception as e:
            print e
            return 0

    def update_description(self, new_description):
        try:
            order = models.Order.objects.get(pk=self.order_id)
            order.additional_info = new_description
            order.save()
            return 1
        except Exception as e:
            print e
            return 0