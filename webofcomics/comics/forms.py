from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comic, Message

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_seller']

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['title', 'author', 'price', 'description', 'image']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'image']
