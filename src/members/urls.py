from django.contrib import admin
from django.urls import path
from .views import UserRegistraion

urlpatterns = [
    path('register/', UserRegistraion.as_view(), name='signup'),
]