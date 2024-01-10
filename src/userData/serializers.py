from rest_framework import serializers
from books.models import Genre, Book, CustomerRating

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer() 
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'genre', 'description','digital']

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRating
        filelds = ['rating']

class UserDataSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    rated_books = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj['user']
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'full_name': user.first_name + user.last_name 
        }

    def get_rated_books(self, obj):
        rated_books = obj['rated_books']
        book_data = []

        for rating in rated_books:
            book = rating.book
            rating_data = {
                'book': BookSerializer(book).data,
                'rating': rating.rating,# Add other CustomerRating fields as needed
            }
            book_data.append(rating_data)

        return book_data