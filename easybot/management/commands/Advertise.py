from ... import models
import traceback
import random
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class Advertise:
    def __init__(self, adCounter=0):
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

    def add_advertise(self, advertise):
        try:
            ad = models.Advertise(title=advertise['title'], text=advertise['description'], image=advertise['image'],
                                  repeat=advertise['repeat'])
            ad.save()
            return True
        except Exception, err:
            print Exception, err
            traceback.print_exc()
            return False

    def getAllCustomers(self):
        customers = models.Customer.objects.filter()
        return customers
