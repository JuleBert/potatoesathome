#home/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
	path('comments/',views.comments, name='comments'),
]