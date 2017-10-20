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

    def add_remove(self, numbers):
        print self.__c_id
        print self.__p_id
        cart = models.Sabad_Kharid.objects.get(cus_id=self.__c_id, p_id=self.__p_id)
        cart.number += numbers
        print cart.number
        if numbers > 0:
            if models.Product.objects.get(id=self.__p_id).numbers >= cart.number:
                print "can add more"
                cart.save()
                return True
            else:
                print "cant add more"
                return False
        elif numbers < 0:
            if cart.number > 0:
                print "can remove more"
                cart.save()
                return True
            else:
                print "cant remove more"
                return False

    def add_to_cart(self):
        try:
            product = models.Product.objects.get(id=self.__p_id)
            customer = models.Customer.objects.get(id=self.__c_id)
            entry = models.Sabad_Kharid(cus_id=customer, p_id=product)
            entry.save()
            return True
        except:
            return False

    def get_object(self):
        return models.Sabad_Kharid.objects.get(p_id=self.__p_id, cus_id=self.__c_id)
