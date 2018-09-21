#pic_tagger/urls.py
from django.urls import path
from . import views

app_name = 'pic_tagger'
urlpatterns = [
    path('',views.pic_tagger, name='pic_tagger'),
]
