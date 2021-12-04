from django.urls import path
from .views import (
    Index,
    About,
    Order,
    OrderConfirmation,
    OrderPayConfirmation)
from . import views


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>/', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    
]