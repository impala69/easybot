from django import forms

class AddProductForm(forms.Form):
    category_name = forms.CharField(label='Category')
    product_name = forms.CharField(label='Product')
    product_text = forms.CharField(label='ProductText')
    product_price = forms.IntegerField(label='ProductPrice')
    product_image = forms.CharField(label='ProductImage')
