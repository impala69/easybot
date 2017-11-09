from ... import models
import random
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

class Advertise:
    def __init__(self, adCounter):
        self.__addCounter = adCounter
    def getAdvertise(self):
        advertises = models.Advertise.objects.filter(repeat__gte=1)
        size = advertises.count()
        if size > 0:
            # counter = self.__addCounter%size
            counter = random.randrange(0, size)
            advertise = advertises[counter]
            advertise.repeat -= 1
            advertise.save()
            return advertise
        else:
            return 0
    def getAllCustomers(self):
        customers = models.Customer.objects.filter()
        return customers
