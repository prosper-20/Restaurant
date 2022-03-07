from unicodedata import name
from django.urls import path
from .views import blog_home, blog_about, blog_category, blog_contact

urlpatterns = [
    path('home/', blog_home, name='home'),
    path("food-single/", blog_about, name="food-single"),
    path("food-category/", blog_category, name="food-category"),
    path("food-contact/", blog_contact, name="contact")
    
]