from unicodedata import name
from django.urls import path
from .views import  HomeView, PostDetailView, blog_about, blog_category, blog_contact, PostCommentView, PostUpdateView, PostCreateView, PostDeleteView
# blog_home 


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("food-single/", blog_about, name="food-single"),
    path("food-category/", blog_category, name="food-category"),
    path("food-contact/", blog_contact, name="contact"),
    path('post/<int:pk>/comment/', PostCommentView.as_view(), name="post_comments"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    
]