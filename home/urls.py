#home/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('comments/', views.comments, name='comments'),
    path('loginandregister/', views.LoginOrRegister.as_view(), name='loginandregister'),
    path('login/', views.CustomLogin.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('changePassword/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html', success_url='home:home'), name='changePassword'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
