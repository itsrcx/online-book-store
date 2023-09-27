from django.contrib import admin
from django.urls import path, include
from books import views 
urlpatterns = [
    path('', views.homeView, name='home'),
    path('category/<str:cats>', views.categoryView, name='category'),
    path('book/<int:book_id>/', views.bookDetail, name='book_detail'),
    path('book/<int:book_id>/submit_rating/', views.submitRating, name='submit_rating'),
    path('cart/', views.cartView, name='cart'),
    path('cart/update/<int:item_id>/', views.cartUpdate, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.cartRemove, name='remove_from_cart'),
    path('checkout/', views.checkoutView, name='checkout'),
]