from django.urls import path
from .views import item_list, checkout
from . import views

urlpatterns = [
    path("home/", views.item_list, name='item_list'),
    path("checkout/", views.checkout, name="checkout"),
    path('product/', views.product, name='product')
]