from typing import List
from django.shortcuts import render
from django.views.generic import ListView
from Order.models import Item


class Blog_Home(ListView):
    model = Item
    template_name = "blog/food-index.html"
    context_object_name = 'items'
