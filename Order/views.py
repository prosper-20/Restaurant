from django.shortcuts import render
from .models import Item


def item_list(request):
    items = Item.objects.all()

    context = {
        'items': items
    }

    return render(request, "Order/home.html", context)
