from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class CommentDataAccess:
    def __init__(self, t_id=None, new_comment=None, cat_id=None, customer_id=None, p_id=None):
        self.__t_id = t_id
        self.__new_comment = new_comment
        self.__cat_id = cat_id
        self.__customer_id = customer_id
        self.__p_id = p_id

    #naghd
    def enter_comment(self):
        try:
            comment = models.Comment(telegram_id=self.__t_id, comment=self.__new_comment, comment_cat=self.__cat_id)
            comment.save()
            return True
        except:
            return False

    def enter_user_comment(self):

        comment = models.Product_comment(customer_id=self.__customer_id,product_id = self.__p_id,text_comment=self.__new_comment)
        comment.save()
        return True


