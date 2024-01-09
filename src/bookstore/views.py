from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from books.models import Book
from .serializers import BookSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.shortcuts import render

@login_required
def generate_api_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    return JsonResponse({'token': token.key})

@login_required
def generate_token_page(request):
    return render(request, 'api_page.html')

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for this view

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for this view