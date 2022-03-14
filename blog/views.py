from typing import List
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from Order.models import Item
from .forms import CommentForm
from .models import Post, Comment
from django.urls import reverse_lazy


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
    context_object_name = "post"
    template_name = "blog/food-single.html"

class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # success_url = "/"
    template_name = "blog/post_comment_form.html"

    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy('post_detail', kwargs={'slug': self.kwargs['slug']})

    # def get_success_url(self):
    #     return reverse_lazy('pk', kwargs={'slug': self.kwargs['id']})
    

def blog_about(request):
    return render(request, "blog/food-single.html")


def blog_category(request):
    return render(request, "blog/food-category.html")

def blog_contact(request):
    return render(request, "blog/food-contact.html")