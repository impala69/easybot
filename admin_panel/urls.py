from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.adding),
    url(r'^adding', views.adding),
    url(r'^showing',views.showing),
    url(r'^enteghadat',views.enteghadat),
    url(r'^category', views.category),
    url(r'^comments',views.comments),
    url(r'^adding',views.adding),
    url(r'^adding/showing/', views.showing),
    url(r'^adding/enteghadat/', views.enteghadat),
    url(r'^adding/category/', views.category),
    url(r'^adding/comments/', views.comments),
    url(r'^orders', views.orders),
    url(r'^editDescription', views.editDescription),
    url(r'^arrived', views.arrived),
    url(r'^deletecomment', views.deletecomment),
    url(r'^edit',views.edit),
    url(r'^edit/showing',views.showing),
    url(r'^delete',views.delete),
    url(r'^delete_cat',views.delete_cat),
    url(r'^adding_cat',views.adding_cat),

    ]