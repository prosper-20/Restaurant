from typing import List
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    fields = ["title", "content"]

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

    fields = ["title", "content"]

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # success_url = "/"
    template_name = "blog/post_comment_form.html"

    def form_valid(self, form):
        form.instance.name = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})
    

def blog_about(request):
    return render(request, "blog/food-single.html")


def blog_category(request):
    return render(request, "blog/food-category.html")

def blog_contact(request):
    return render(request, "blog/food-contact.html")