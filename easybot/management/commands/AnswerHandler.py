from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class AnswerHandler:
    def __init__(self, question_id=None, question_answer=None):
        self.__question_id = question_id
        self.__question_answer = question_answer

    def add_answer(self):
        try:
            new_answer = models.Answers(question_id=self.get_question_object(), text=self.__question_answer)
            new_answer.save()
            return 1
        except Exception as e:
            print e
            return 0
    def get_question_object(self):
        try:
            return models.Questions.objects.get(pk=self.__question_id)
        except Exception as e:
            print e
            return 0




