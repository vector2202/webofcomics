from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comic, Wishlist, Notification, Message
from .forms import ComicForm, MessageForm

def home(request):
    comics = Comic.objects.all()
    return render(request, 'comics/home.html', {'comics': comics})

@login_required
def register_comic(request):
    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.seller = request.user
            comic.save()
            return redirect('home')
    else:
        form = ComicForm()
    return render(request, 'comics/register_comic.html', {'form': form})

@login_required
def add_to_wishlist(request, comic_id):
    comic = Comic.objects.get(id=comic_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.comics.add(comic)
    return redirect('home')

@login_required
def send_message(request, comic_id):
    comic = Comic.objects.get(id=comic_id)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = comic.seller
            message.comic = comic
            message.save()
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'comics/send_message.html', {'form': form, 'comic': comic})

