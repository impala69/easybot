from easybot import models
from admin_panel import FormsHandler


class SurveyManager:
    def __init__(self, survey_data=None, deleted_survey_id=None, deleted_question_id=None):
        self.survey_data = survey_data
        self.deleted_survey_id = deleted_survey_id
        self.deleted_question_id = deleted_question_id

    def get_all_surveys(self):
        all_surveys = models.Surveys.objects.all()
        all_surveys_data = []
        for survey in all_surveys:
            # add one survey data in dictionary
            # example: {u'questions': [{u'text': u'test1', u'id': 49}, {u'text': u'test2', u'id': 50}], u'title': u'test yeah'}
            survey_data = {}
            # survey contains title
            survey_data['id'] = survey.pk
            survey_data['title'] = survey.title
            all_questions = models.Questions.objects.filter(survey_id=survey)
            all_questions_data_list = []
            for question in all_questions:
                question_data = {}
                question_data['id'] = question.pk
                question_data['text'] = question.text
                all_questions_data_list.append(question_data)
            all_surveys_data.append(survey_data)
            # survey contains questions
            survey_data['questions'] = all_questions_data_list
        return all_surveys_data

    def add_survey(self):
        add_survey_form = FormsHandler.AddSurveyForm(self.survey_data)
        if add_survey_form.is_valid():
            survey_title = add_survey_form.cleaned_data['survey_title']
            question_inputs = self.survey_data.getlist('questions[]')  # this list conatins all questions
            questions = []
            for i in range(len(question_inputs)):
                questions.append((question_inputs[i].encode('utf8')))
            try:
                new_survey = models.Surveys(title=survey_title)
                new_survey.save()
                for question in questions:
                    new_question = models.Questions(survey_id=new_survey, text=question)
                    new_question.save()
                return 1
            except Exception as e:
                print e
                return 0

    def delete_survey(self):
        try:
            models.Surveys.objects.get(pk=self.deleted_survey_id).delete()
            return 1
        except Exception as e:
            print e
            return 0

    def delete_question(self):
        try:
            models.Questions.objects.get(pk=self.deleted_question_id).delete()
            return 1
        except Exception as e:
            print e
            return 0
