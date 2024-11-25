from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register_comic/', views.register_comic, name='register_comic'),
    path('comic/<int:comic_id>/', views.comic_detail, name='comic_detail'),
    path('comic/<int:comic_id>/update/', views.update_comic, name='update_comic'),
    path('comic/<int:comic_id>/delete/', views.delete_comic, name='delete_comic'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:comic_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:comic_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('send_message/<int:comic_id>/', views.send_message, name='send_message'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
