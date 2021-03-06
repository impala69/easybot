from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import telepot, time
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

class CategoryDataAccess:
    def __init__(self):
        pass

    def get_cats(self):
        result = models.Category.objects.filter()
        return result

    def feed_back_cat_keyboard(self):
        list1 = []
        for item in models.Feedback_cat.objects.all():
            name = item.fb_name
            cat_keyboard = [InlineKeyboardButton(text=name, callback_data='naghd' + str(item.pk))]
            list1.append(cat_keyboard)
        cat_keyboard = InlineKeyboardMarkup(inline_keyboard=list1)
        return cat_keyboard

    def add_category(self, category_title):
            try:
                new_category = models.Category(cat_name=category_title)
                new_category.save()
                return 1
            except Exception as e:
                print e
                return 0


