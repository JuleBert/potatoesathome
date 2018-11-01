# home/views.py
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm
from .tokens import account_activation_token


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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your potatoesathome account'
            message = render_to_string('home/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('home:login')
    else:
        form = SignUpForm()
    return render(request, 'home/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        # uid = urlsafe_base64_decode(uidb64).decode()
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home:home')
    else:
        return render(request, 'home/account_activation_invalid.html')