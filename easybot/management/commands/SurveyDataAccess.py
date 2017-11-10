from ... import models
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class SurveyDataAccess:
    def __init__(self, survey_id=None):
        self.__survey_id = survey_id

    def get_all_survey(self):
        try:
            surveys = models.Surveys.objects.all()
            all_surveys = []
            for survey in surveys:
                survey_data = {}
                survey_data['id'] = survey.pk
                survey_data['title'] = survey.title
                all_surveys.append(survey_data)
            return all_surveys
        except Exception as e:
            print e
            return 0

    def get_survey_questions(self):
        try:
            survey = models.Surveys.objects.get(pk=self.__survey_id)
            questions = models.Questions.objects.get(survey_id=survey)
            all_questions = []
            for question in questions:
                question_data = {}
                question_data['id'] = question.pk
                question_data['text'] = question.text
                all_questions.append(question_data)
            return all_questions
        except Exception as e:
            print e
            return 0

    def get_number_of_questions(self):
        try:
            survey_object = models.Surveys.objects.get(pk=self.__survey_id)
            numebr_of_questions = models.Questions.objects.filter(survey_id=survey_object).count()
            return numebr_of_questions
        except Exception as e:
            print e
            return 0

    def get_question_data(self, question_order):
        try:
            survey_object = models.Surveys.objects.get(pk=self.__survey_id)
            question = models.Questions.objects.get(survey_id=survey_object)[question_order-1]

        except Exception as e:
            print e
            return 0





