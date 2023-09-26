from django.contrib import admin
from django.urls import path, include
from books import views 
urlpatterns = [
    path('', views.homeView, name='home'),
    path('book/<int:book_id>/', views.bookDetail, name='book_detail'),
    path('book/<int:book_id>/submit_rating/', views.submitRating, name='submit_rating'),
    path('cart/', views.cartView, name='cart'),
    path('checkout/', views.checkoutView, name='checkout'),
]