from django.urls import path
from .views import blog_home, blog_about

urlpatterns = [
    path('home/', blog_home, name='home'),
    path("food-single/", blog_about, name="food-single")
    
]