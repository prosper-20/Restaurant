from typing import List
from django.shortcuts import render
from django.views.generic import ListView
from Order.models import Item


def blog_home(request):
    items = Item.objects.all()[0:12]
    context = {
        "items": items,
    }
    return render(request, "blog/index.html", context)

def blog_about(request):
    return render(request, "blog/food-single.html")