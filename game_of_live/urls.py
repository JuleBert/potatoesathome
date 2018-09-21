#game_of_live/urls.py
from django.urls import path
from . import views

app_name = 'game_of_live'
urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
]
