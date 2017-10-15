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
    url(r'^adding/adding',views.adding),
    url(r'^adding/showing', views.showing),
    url(r'^adding/enteghadat', views.enteghadat),
    url(r'^adding/category', views.category),
    url(r'^adding/comments', views.comments),

    ]