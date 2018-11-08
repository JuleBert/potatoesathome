#home/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('comments/', views.comments, name='comments'),
    path('login/', views.CustomLogin.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),

    # signup / register
    path('signup/', views.signup, name='signup'),
    path('loginandregister/', views.LoginOrRegister.as_view(), name='loginandregister'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('changePassword/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('home:home')), name='passwordChange'),

    # password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url = reverse_lazy('home:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy('home:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
