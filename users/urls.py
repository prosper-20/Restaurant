from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
from users.views import register


urlpatterns = [
    path('', users_views.register1, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)