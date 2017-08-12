from django import forms

class AddProductForm(forms.Form):
    category_name = forms.CharField(label='Category' , max_length=30)
    product_name = forms.CharField(label='Product' , max_length=30)
    product_text = forms.CharField(label='ProductText' , max_length=60)
    product_price = forms.IntegerField(label='ProductPrice')
    product_image = forms.CharField(label='ProductImage' , max_length=30)
