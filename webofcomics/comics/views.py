from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Comic, Wishlist, Notification, Message, User
from .forms import ComicForm, MessageForm
from .forms import UserRegistrationForm

@login_required
def home(request):
    query = request.GET.get('q')
    comics = Comic.objects.all()
    if query:
        comics = comics.filter(title__icontains=query)
    return render(request, 'home/home.html', {'comics': comics})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'login/register/register.html', {'form': form})

@login_required
def register_comic(request):
    if request.method == 'POST':
        comic_form = ComicForm(request.POST, request.FILES)
        print(comic_form)
        print(comic_form)
        print("Form errors:", comic_form.errors)
        if comic_form.is_valid():
            print("Saving comic")
            comic = comic_form.save(commit=False)
            comic.seller = request.user
            comic.save()
            return redirect('home')
    else:
        comic_form = ComicForm()
    return render(request, 'comics/register_comic.html', {'form': comic_form})

@login_required
def update_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    if comic.seller != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES, instance=comic)
        print("UPDATE")
        print("Form errors:", form.errors)
        
        if form.is_valid():
            form.save()
            return redirect('comic_detail', comic_id=comic.id)
    else:
        form = ComicForm(instance=comic)
    return render(request, 'comics/update_comic.html', {'form': form, 'comic': comic})

@login_required
def delete_comic(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    if comic.seller != request.user:
        return redirect('home')
    if request.method == 'POST':
        comic.delete()
        return redirect('home')
    return render(request, 'comics/delete_comic.html', {'comic': comic})

@login_required
def comic_detail(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    return render(request, 'detail/comic_detail.html', {'comic': comic})

@login_required
def wishlist(request):
    try:
        wishlist = request.user.wishlist
        wishlist_items = wishlist.comics.filter(id__isnull=False)
    except:
        wishlist_items = None
    print(f"Wishlist items: {wishlist_items}")
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, comic_id):
    comic = Comic.objects.get(id=comic_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    wishlist.comics.add(comic)
    return redirect('home')

@login_required
def remove_from_wishlist(request, comic_id):
    comic = get_object_or_404(Comic, id=comic_id)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    if wishlist:
        wishlist.comics.remove(comic)
    return redirect('wishlist')

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
    return render(request, 'messages/send_message.html', {'form': form, 'comic': comic})


@login_required
def messages_list(request):
    sent_conversations = Message.objects.filter(sender=request.user).values('receiver', 'comic').distinct()
    received_conversations = Message.objects.filter(receiver=request.user).values('sender', 'comic').distinct()
    conversations = list(sent_conversations) + list(received_conversations)

    conversations_cleaned = []
    for convo in conversations:
        other_user_id = convo.get('receiver') or convo.get('sender')  # Obtener el otro usuario
        other_user = User.objects.get(id=other_user_id)  # Obtener el usuario completo
        comic = Comic.objects.get(id=convo['comic'])  # Obtener el cómic completo
        conversations_cleaned.append({'user': other_user, 'comic': comic})
    return render(request, 'messages/message_list.html', {
        'conversations': conversations_cleaned,
    })

@login_required
def messages_with_user_comic(request, user_id, comic_id):
    selected_user = get_object_or_404(User, id=user_id)
    selected_comic = get_object_or_404(Comic, id=comic_id)
    messages = Message.objects.filter(
        sender=request.user, receiver=selected_user, comic=selected_comic
    ) | Message.objects.filter(
        sender=selected_user, receiver=request.user, comic=selected_comic
    )
    messages = messages.order_by('sent_at')
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        Message.objects.create(
            sender=request.user,
            receiver=selected_user,
            comic=selected_comic,
            text=text,
            image=image
        )
        return redirect('messages_with_user_comic', user_id=user_id, comic_id=comic_id)

    

    return render(request, 'messages/message_list.html', {
        'selected_user': selected_user,
        'selected_comic': selected_comic,
        'messages': messages
    })
