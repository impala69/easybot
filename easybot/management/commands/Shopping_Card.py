from ... import models

class ShoppingCard:
    def __init__(self , c_id , p_id= None):
        self.__c_id = c_id
        self.__p_id = p_id

    def sabad_from_customer(self):
           rows = models.Sabad_Kharid.objects.filter(cus_id=self.__c_id)
           products = [[item.p_id,item.number] for item in rows]
           return products

    def del_from_cart(self):
        cart = models.Sabad_Kharid.objects.filter(cus_id=self.__c_id)
        count0 = models.Sabad_Kharid.objects.filter(cus_id=self.__c_id).count()
        cart = cart.filter(p_id=self.__p_id)
        count = cart.filter(p_id=self.__p_id).count()
        if count0 == 0 or count == 0:
            return False
        else:
            cart.delete()
            return True

    def add_remove(self,numbers):
        cart = models.Sabad_Kharid.objects.filter(cus_id=self.__c_id, p_id=self.__c_id)


    def add_to_cart(self):
        try:
            product = models.Product.objects.get(id=self.__p_id)
            customer = models.Customer.objects.get(id=self.__c_id)
            entry = models.Sabad_Kharid(cus_id=customer, p_id=product)
            entry.save()
            return True
        except:
            return False