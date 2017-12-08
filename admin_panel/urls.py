from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.add_product),
    url(r'^add_product', views.add_product),
    url(r'^product', views.show_product),
    url(r'^show_products', views.show_products),
    url(r'^enteghadat', views.enteghadat),
    url(r'^category', views.category),
    url(r'^comments', views.show_product_comments),
    url(r'^add_feed_cat', views.add_feedback_category),
    url('orders/peyk_add', views.peyk_motori_add),
    url('orders/del_order', views.del_order),
    url('orders/inpeyk', views.inpeyk),
    url('orders/arrived', views.arrived),
    url('orders', views.orders),
    url(r'^editDescription', views.editDescription),
    url(r'^deletecomment', views.deletecomment),
    url(r'^edit',views.edit),
    url(r'^delete_product',views.delete_product),
    url(r'^del_cat',views.del_cat),
    url(r'^add_cat',views.add_cat),
    url(r'^del_cat',views.del_cat),
    url(r'^add_cat',views.add_cat),
    url(r'^cm_del',views.cm_del),
    url(r'^show_feedback_categories',views.show_feedback_categories),
    url(r'^delete_feedback',views.delete_feedback),
    url(r'^ed_cat',views.ed_cat),
    url(r'^survey',views.survey),
    url(r'^show_survey',views.show_survey),
    url(r'^add_advertise', views.add_advertise),
    url(r'^advertise', views.advertise),
    url(r'^add_ad',views.add_advertise),
    url(r'^del_ad', views.del_ad),
    url(r'^add_code', views.add_code),
    url(r'^codes', views.codes),
    url(r'^del_code', views.del_code),
    url(r'^del_survey',views.del_survey),
    url(r'^del_question',views.del_question),
    ]
