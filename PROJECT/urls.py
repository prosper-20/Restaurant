"""PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from Core import views
from Core.views import Menu, MenuSearch,home_page
from users import views as user_views
from users.views import register, profile_edit
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from Order.views import dentist_view, reservation_view, appointment


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("Core.urls")),
    path('blog/', include('blog.urls')),
    path('order/', include("Order.urls")),
    path('accounts/', include('allauth.urls')),
    path('home-page/', views.home_page, name="home_page"),
    path("restaurant/", include('restaurant.urls')),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('register/', include("users.urls")),
    path("register1/", user_views.register1, name="register1"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path("profile/edit/", user_views.profile_edit, name="profile_edit"),
    path("dentist/", dentist_view, name="dentist"),
    path('reservation/', reservation_view.as_view(), name='reservation'),
    path('appointment.html', appointment, name='appointment')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
