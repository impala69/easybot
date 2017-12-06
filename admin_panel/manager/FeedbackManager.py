from easybot import models
from admin_panel import FormsHandler


class FeedbackManager:
    def __init__(self, feedback_category_data=None, deleted_naghd_id=None):
        self.feedback_category_data = feedback_category_data
        self.deleted_naghd_id = deleted_naghd_id

    def get_all_feedback_categories(self):
        result = models.Feedback_cat.objects.filter()
        cat_data = []
        all_cat = []
        for cat in result:
            cat_data.append(cat.pk)
            cat_data.append(cat.fb_name)
            all_cat.append(cat_data)
            cat_data = {}

        return all_cat

    def add_feedback_category(self):
        add_feed_cat = FormsHandler.AddCategoryForm(self.feedback_category_data)
        if add_feed_cat.is_valid():
            category_name = add_feed_cat.cleaned_data['category_name']
            try:
                new_category = models.Feedback_cat(fb_name=category_name)
                new_category.save()
                return 1
            except Exception as e:
                print('error')
                print e
                return 0
        else:
            print "Not Valid Form Adding FeedBack Category!"
            return 0

    def delete_feddback_category(self):
        try:
            models.Feedback_cat.objects.get(pk=self.deleted_naghd_id).delete()
            return 1
        except Exception as e:
            print e
            return 0
