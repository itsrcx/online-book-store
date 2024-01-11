from rest_framework import serializers
from books.models import Book, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True) 
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'genre', 'description', 'quantity', 'digital']
