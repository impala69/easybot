from django import forms

class AddProductForm(forms.Form):
    category_name = forms.CharField(label='Category' , max_length=30)
    product_name = forms.CharField(label='Product' , max_length=30)
    product_text = forms.CharField(label='ProductText' , max_length=60)
    product_price = forms.IntegerField(label='ProductPrice')
    product_image = forms.CharField(label='ProductImage' , max_length=30)

class EditProductForm(forms.Form):
    pic_form = forms.CharField(max_length=30, label='ProductImage')
    price_form = forms.IntegerField(label="ProductPrice")
    detail_form = forms.CharField(label='ProductText', max_length=30)
    name_form = forms.CharField(label="Product", max_length=30)
