from easybot import models
from admin_panel import FormsHandler


class CategoryManager:
    def __init__(self, category_data=None, deleted_category_id=None, category_id=None):
        self.category_data = category_data
        self.deleted_category_id = deleted_category_id
        self.category_id = category_id

    def get_all_categories(self):
        result = models.Category.objects.filter()
        cat_data = []
        all_cat = []
        for cat in result:
            cat_data.append(cat.pk)
            cat_data.append(cat.cat_name)
            all_cat.append(cat_data)
            cat_data = []

        return all_cat

    def add_category(self):
        add_cat_form = FormsHandler.AddCategoryForm(self.category_data)
        if add_cat_form.is_valid():
            category_name = add_cat_form.cleaned_data['category_name']
            try:
                new_category = models.Category(cat_name=category_name)
                new_category.save()
                return 1
            except Exception as e:
                print e
                return 0
        else:
            print('Failed Adding Category!')
            return 0

    def delete_category(self):
        try:
            models.Category.objects.get(pk=self.deleted_category_id).delete()
            return 1
        except Exception as e:
            print e
            return 0

    def get_category_object(self):
        try:
            return models.Category.objects.get(pk=self.category_id)
        except Exception as e:
            print e
            return 0
