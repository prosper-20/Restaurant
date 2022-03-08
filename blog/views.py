from typing import List
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from Order.models import Item
from .models import Post


# def blog_home(request):
#     items = Item.objects.all()[0:12]
#     context = {
#         "items": items,
#     }
#     return render(request, "blog/index.html", context)


class HomeView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/index.html"
    ordering = ["-date_posted"]

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/food-single.html"
    

def blog_about(request):
    return render(request, "blog/food-single.html")


def blog_category(request):
    return render(request, "blog/food-category.html")

def blog_contact(request):
    return render(request, "blog/food-contact.html")