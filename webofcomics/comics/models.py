from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_seller = models.BooleanField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
class Comic(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comics')
class ComicImage(models.Model):
    comic = models.ForeignKey(Comic, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    comics = models.ManyToManyField(Comic, blank=True)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="comic")
    text = models.TextField()
    image = models.ImageField(upload_to='messages/', null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

