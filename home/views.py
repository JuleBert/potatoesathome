# home/views.py
from django.shortcuts import render
from django.utils import timezone

from .models import Post
from .forms import PostForm

# Create your views here.
def home(request):
    context = {
        'user': 'User 23'
    }
    return render(request, 'home/home.html', context)
	
def menu(request):
    context = {
        'user': 'User 23'
    }
    return render(request, 'base.html', context)

def comments(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    form = PostForm()
    context = {'form': form,
               'posts':posts}
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
            form = PostForm()
            context = {'form': form,
                       'posts': posts}
            return render(request, 'home/comments.html', context)
    return render(request, 'home/comments.html', context)