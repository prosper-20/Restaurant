from unicodedata import name
from django.urls import path
from .views import blog_about, blog_category, blog_contact, HomeView
# blog_home


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path("food-single/", blog_about, name="food-single"),
    path("food-category/", blog_category, name="food-category"),
    path("food-contact/", blog_contact, name="contact")
    
]