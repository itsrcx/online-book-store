from django.contrib import admin
from django.urls import path
from .views import UserRegistraion, CustomLoginView

urlpatterns = [
    path('register/', UserRegistraion.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login')
]