from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import Dashboard, OrderDetails
from Core.views import new_home, clone_new_home
from Core import views

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order/<int:pk>/', OrderDetails.as_view(), name='order-details'),
    path('index/', views.new_home, name="new_home" ),
    path('clone/', views.clone_new_home, name="clone_home")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)