from unicodedata import name
from django.urls import path
from .views import  HomeView, PostDetailView, blog_about, blog_category, blog_contact, PostCommentView
# blog_home 


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path("post/<slug>/", PostDetailView.as_view(), name="post_detail"),
    path("food-single/", blog_about, name="food-single"),
    path("food-category/", blog_category, name="food-category"),
    path("food-contact/", blog_contact, name="contact"),
    path('post/<slug>/comment/', PostCommentView.as_view(), name="post_comments"),

    
]