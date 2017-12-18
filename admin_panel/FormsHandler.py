from django import forms


class AddProductForm(forms.Form):
    category_name = forms.CharField(label='Category', max_length=30)
    product_name = forms.CharField(label='Product', max_length=30)
    product_text = forms.CharField(label='ProductText')
    product_price = forms.IntegerField(label='ProductPrice')
    product_image = forms.ImageField()


class EditProductForm(forms.Form):
    product_image = forms.CharField(max_length=30, label='ProductImage')
    product_price = forms.IntegerField(label="ProductPrice")
    product_text = forms.CharField(label='ProductText', max_length=30)
    product_name = forms.CharField(label="Product", max_length=30)
    product_number = forms.IntegerField(label="ProductNumber")
    category_name = forms.CharField(label='Category', max_length=30)


class AddCategoryForm(forms.Form):
    category_name = forms.CharField(label="Category" , max_length=30)


class AddSurveyForm(forms.Form):
    survey_title = forms.CharField(max_length=30, label='SurveyTitle')


class AddAdvertiseForm(forms.Form):
    advertise_title = forms.CharField(label="Advertise Title", max_length=300)
    advertise_text = forms.CharField(widget=forms.Textarea)
    advertise_image = forms.ImageField()


class AddCodeForm(forms.Form):
    code_char = forms.CharField(label="Code Char", max_length=30)


class AddPeykForm(forms.Form):
    peyk_first_name = forms.CharField(label="firstName", max_length=30)
    peyk_last_name = forms.CharField(label="lastName", max_length=30)
    peyk_phone = forms.CharField(label="phone", max_length=30)
    order_id = forms.IntegerField(label="OrderNumber")




