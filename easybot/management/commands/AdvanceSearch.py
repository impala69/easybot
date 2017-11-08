from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class AdvanceSearchDataAccess:

    def __init__(self,search_word , priceMin = 0, priceMax = 999999999):
        self.__search_word = search_word
        self.__priceMin = priceMin
        self.__priceMax = priceMax

    def searchAll(self):
        result = models.Product.objects.filter(product_name__icontains=self.__search_word, price__lte=self.__priceMax, price__gte=self.__priceMin).order_by('id').values('id')
        return result

    def searchAvalable(self):
        result = models.Product.objects.filter(product_name__icontains=self.__search_word, price__lte=self.__priceMax, price__gte=self.__priceMin, numbers__gt=0).order_by('id').values('id')
        return result
