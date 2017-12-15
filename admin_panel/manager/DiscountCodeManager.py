from easybot import models
from admin_panel import FormsHandler


class DiscountCodeManager:
    def __init__(self, code_data=None, deleted_code_id=None):
        self.code_data = code_data
        self.deleted_code_id = deleted_code_id

    def get_all_discount_code(self):
        result = models.DiscountCode.objects.filter()
        code_data = {}
        all_codes = []
        for one_code in result:
            code_data['code_id'] = one_code.pk
            code_data['code_char'] = one_code.code_char
            all_codes.append(code_data)
            code_data = {}
        return all_codes

    def add_discount_code(self):
        add_code_form = FormsHandler.AddCodeForm(self.code_data)
        if add_code_form.is_valid():
            code_char = add_code_form.cleaned_data['code_char']
            try:
                new_code = models.DiscountCode(code_char=code_char)
                new_code.save()
                return 1
            except Exception as e:
                print e
                return 0
        else:
            return 0

    def delete_code(self):
        try:
            models.DiscountCode.objects.get(pk=self.deleted_code_id).delete()
            return 1
        except Exception as e:
            print e
            return 0
