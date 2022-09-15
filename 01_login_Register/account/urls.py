from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from account import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
