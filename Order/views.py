from django.db import models
from django.shortcuts import render
from .models import Item
from django.views.generic import ListView, DetailView


class HomeView(ListView):
    model = Item
    template_name = 'Order/new_home_page.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'Order/product-page.html'

def item_list(request):
    items = Item.objects.all()

    context = {
        'items': items
    }

    return render(request, "Order/new_home_page.html", context)

def checkout(request):
    return render(request, "Order/checkout-page.html")

def product(request):
    return render(request, "Order/product-page.html")
