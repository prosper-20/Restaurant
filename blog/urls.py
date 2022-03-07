from django.urls import path
from .views import blog_home, blog_about, blog_category

urlpatterns = [
    path('home/', blog_home, name='home'),
    path("food-single/", blog_about, name="food-single"),
    path("food-category/", blog_category, name="food-category"),
    
]