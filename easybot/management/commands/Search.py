from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class SearchDataAccess:

    def __init__(self, search_word, page_number):
        self.__search_word = search_word
        self.__page_number = page_number

    def search(self):
        if self.__page_number == 1:
            result = models.Product.objects.filter(product_name__icontains=self.__search_word).order_by('id').values('id')[:10]
            return result
        else:
            offset = (self.__page_number-1)*10
            result = models.Product.objects.filter(product_name__icontains=self.__search_word).order_by('id').values('id')[offset:offset+9]
            return result
