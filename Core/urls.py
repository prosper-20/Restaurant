from django.urls import path
from .views import (
    Index,
    About,
    Order,
    Test_Order,
    OrderConfirmation,
    OrderPayConfirmation,
    home_page)
from . import views


urlpatterns = [
    path('', views.home_page, name='index'),
    path('about/', About.as_view(), name='about'),
    path('order/', Order.as_view(), name='order'),
    path('test-order/', Test_Order.as_view(), name="test_order"),
    path('order-confirmation/<int:pk>/', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    
]