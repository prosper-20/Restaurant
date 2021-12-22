from django.shortcuts import render
from .models import Item


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
