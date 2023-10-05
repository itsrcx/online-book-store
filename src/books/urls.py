from django.contrib import admin
from django.urls import path
from books import views 
urlpatterns = [
    path('', views.homeView, name='home'),
    path('category/<slug:slug>', views.categoryView, name='category'),
    path('book/<str:slug>/', views.bookDetail, name='book_detail'),
    path('book/<str:slug>/submit_rating/', views.submitRating, name='submit_rating'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<str:slug>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/checkout', views.checkoutView, name='checkout'),
    path('add_address/', views.add_shipping_address, name='add_shipping_address'),
    path('set_default_address/<int:address_id>/', views.set_default_address, name='set_default_address'),
    path('order_history/', views.order_history, name='order_history'),

]