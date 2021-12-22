from django.urls import path
from .views import (
    item_list, 
    checkout, 
    HomeView,
    ItemDetailView
)
from . import views

urlpatterns = [
    path("home/", HomeView.as_view(), name='item_list'),
    path("checkout/", views.checkout, name="checkout"),
    path('product/<slug>/', ItemDetailView.as_view(), name='product')
]