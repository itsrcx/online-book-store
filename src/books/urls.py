from django.contrib import admin
from django.urls import path, include
from . import views 
urlpatterns = [
    path('', views.homeView, name='home'),
    path('cart/', views.cartView, name='cart'),
    path('checkout/', views.checkoutView, name='checkout'),
]