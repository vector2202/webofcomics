from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register_comic/', views.register_comic, name='register_comic'),
    path('add_to_wishlist/<int:comic_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('send_message/<int:comic_id>/', views.send_message, name='send_message'),
]