from django.urls import path
from .views import item_list
from . import views

urlpatterns = [
    path("home/", views.item_list, name='item_list')
]