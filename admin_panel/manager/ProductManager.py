from easybot import models
from admin_panel import FormsHandler
import CategoryManager


class ProductManager:
    def __init__(self, product_data=None, image_data=None, deleted_product_id=None, category_id=None, product_id=None):
        self.product_data = product_data
        self.deleted_product_id = deleted_product_id
        self.category_id = category_id
        self.image_data = image_data
        self.product_id = product_id

    def get_all_products(self):
        result = models.Product.objects.all()
        product_data = []
        all_product = []
        for product in result:
            product_data.append(product.pk)
            product_data.append(product.cat_id)
            product_data.append(product.product_name)
            product_data.append(product.text)
            product_data.append(product.image)
            product_data.append(product.price)
            all_product.append(product_data)
            product_data = []
        return all_product

    def add_product(self):
        adding_form = FormsHandler.AddProductForm(self.product_data, self.image_data)
        if adding_form.is_valid():
            category_object = CategoryManager.CategoryManager(category_id=adding_form.cleaned_data['category_name'])
            product_name = adding_form.cleaned_data['product_name']
            text = adding_form.cleaned_data['product_text']
            image = adding_form.cleaned_data['product_image']
            price = adding_form.cleaned_data['product_price']
            try:
                new_product = models.Product(cat_id=category_object.get_category_object(), product_name=product_name, text=text, image=image,
                                             price=price)
                new_product.save()
                return 1

            except Exception as e:
                print('Faield in Adding Product!')
                print e
                return 0

    def delete_product(self):
        try:
            models.Product.objects.get(pk=self.deleted_product_id).delete()
            return 1
        except Exception as e:
            print e
            return 0

    def get_product_data(self):
        product = models.Product.objects.get(pk=self.product_id)
        product_dict = {'product_id': product.pk, 'Name': product.product_name, 'Price': product.price,
                        'Text': product.text, 'Image': product.image, 'Number': product.numbers}
        return product_dict
