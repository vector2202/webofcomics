from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comic, Message, ComicImage

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_seller', 'phone_number']

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['title', 'author', 'price', 'description']



class ComicImageForm(forms.Form):
    class Meta:
        model = ComicImage
        fields = ['image']
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'image']
