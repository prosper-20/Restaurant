from typing import List
from django.shortcuts import render
from django.views.generic import ListView
from Order.models import Item


def blog_home(request):
    items = Item.objects.all()[1:3]
    context = {
        "items": items,
    }
    return render(request, "blog/food-index.html", context)