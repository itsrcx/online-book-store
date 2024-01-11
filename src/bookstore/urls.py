from django.urls import path
from .views import BookList, BookDetail, generate_api_token, generate_token_page

app_name = 'bookstore' 

urlpatterns = [
    path('generate-token-page/', generate_token_page, name='generate_token_page'),
    path('generate-api-token/', generate_api_token, name='generate_api_token'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]

# api call for the user root
# curl -H "Authorization: Token a7cdb0fd1a4664b9d744e4b51a70146586f55a5b" http://localhost:8000/api/v1/books/{23}/