from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class Advertise:
    def __init__(self, adCounter):
        self.__addCounter = adCounter
    def getAdvertise(self):
        advertises = models.Advertise.objects.filter()
        size = advertises.count()
        counter = self.__addCounter%size
        return advertises[counter]
    def getAllCustomers(self):
        customers = models.Customer.objects.filter()
        return customers
