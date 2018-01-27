from ... import models
import traceback
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class ProductDataAccess:
    def __init__(self, page_number=None, cat_id=None, p_id=None, t_id=None):
        self.__cat_id = cat_id
        self.__p_id = p_id
        self.__t_id = t_id
        self.__page_number = page_number

    def get_product_from_category(self):
        if self.__page_number == 1:
            result = models.Product.objects.filter(cat_id=self.__cat_id).order_by('id').values('id')[:10]
            return result
        else:
            offset_val = (self.__page_number - 1) * 10
            result = models.Product.objects.filter(cat_id=self.__cat_id).order_by('id').values('id')[:offset_val + 9]
            return result

    def add_product(self, product):
        try:
            pr = models.Product(product_name=product['title'], text=product['description'], image=product['image'],
                                price=product['price'], cat_id_id=product['cat_id'],
                                numbers=product['number'])
            pr.save()
            return True
        except Exception, err:
            print Exception, err
            traceback.print_exc()
            return False

    def show_product(self):
        product = models.Product.objects.get(pk=self.__p_id)
        product_dict = {'product_id': product.pk, 'Name': product.product_name, 'Image': product.image,
                        'Text': product.text, 'Price': product.price}
        return product_dict

    def like(self):
        product = models.Product.objects.get(id=self.__p_id)
        try:
            entry = models.Like_dislike(telegram_id=self.__t_id, p_id=product, like=True)
            entry.save()
            print "adding like"
            return True
        except:
            entry = models.Like_dislike.objects.get(telegram_id=self.__t_id, p_id=product)
            if (entry.like):
                print "clearing like"
                entry.delete()
                return False
            else:
                print "changing dislike to like"
                entry.like = True
                entry.save()
                return True

    def dislike(self):
        product = models.Product.objects.get(id=self.__p_id)
        try:
            entry = models.Like_dislike(telegram_id=self.__t_id, p_id=product, like=False)
            entry.save()
            print "adding dislike"
            return True
        except:
            entry = models.Like_dislike.objects.get(telegram_id=self.__t_id, p_id=product)
            if (not entry.like):
                print "clearing dislike"
                entry.delete()
                return False
            else:
                print "changing like to dislike "
                entry.like = False
                entry.save()
                return True

    def get_likes(self):
        return models.Like_dislike.objects.filter(p_id=self.__p_id, like=True).count()

    def get_dislikes(self):
        return models.Like_dislike.objects.filter(p_id=self.__p_id, like=False).count()
