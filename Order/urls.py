from django.urls import path
from .views import (
    HomeView,
    ItemDetailView,
    add_to_cart, remove_from_cart,
    OrderSummaryView,
    remove_single_item_from_cart,
    CheckoutView,
    PaymentView,
    AddCouponView,
    RequestRefundView,
    snacks_view,
    maincourse_view,
    appetizers_view,
    desserts_view,
    NewConfirmationView,
)
from . import views

urlpatterns = [
    path("home/", HomeView.as_view(), name='item_list'),
    # path("checkout/", views.checkout, name="checkout"),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path("add-coupon/", AddCouponView.as_view(), name="add_coupon"),
    path('order-summary/', OrderSummaryView.as_view(), name="order_summary"),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment/<str:payment_option>/", PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request_refund'),
    path('snacks/', views.snacks_view, name="snacks"),
    path('maincourse/', views.maincourse_view, name="main_course"),
    path('appetizers/', views.appetizers_view, name="appetizers"),
    path('desserts/', views.desserts_view, name="desserts"),
    path('new-confirm/', NewConfirmationView.as_view(), name="new"),

]