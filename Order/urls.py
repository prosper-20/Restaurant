from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    add_to_cart, remove_from_cart,
    OrderSummaryView,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    add_coupon
)
from . import views

urlpatterns = [
    path("home/", HomeView.as_view(), name='item_list'),
    # path("checkout/", views.checkout, name="checkout"),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path("add-coupon/<code>/", add_coupon, name="add_coupon"),
    path('order-summary/', OrderSummaryView.as_view(), name="order_summary"),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment/<str:payment_option>/", PaymentView.as_view(), name='payment')
]