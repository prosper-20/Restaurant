from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    add_to_cart
)
from . import views

urlpatterns = [
    path("home/", HomeView.as_view(), name='item_list'),
    # path("checkout/", views.checkout, name="checkout"),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart')
]