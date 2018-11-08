#time_tracking/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'time_tracking'

urlpatterns = [
	#path('', views.input, name='input'),
    path('', views.InputView.as_view(), name='input'),
    path('<int:pk>/', views.TimeDetailView.as_view(), name='time_detail'),
    path('time_list/', views.TimeListView.as_view(), name='time_list'),
    path('new_project/', views.NewProject.as_view(), name='new_project'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('overtime/', views.Overtime.as_view(), name='overtime'),
]