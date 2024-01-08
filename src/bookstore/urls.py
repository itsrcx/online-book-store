from django.urls import path
from .views import BookList, BookDetail

app_name = 'bookstore' 

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]
