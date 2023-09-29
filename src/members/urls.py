from django.contrib import admin
from django.urls import path
from .views import UserRegistraion, CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', UserRegistraion.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]