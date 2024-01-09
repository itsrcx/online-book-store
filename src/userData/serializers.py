from rest_framework import serializers
from books.models import Genre, Book, CustomerRating

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = '__all__'

class CustomerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRating
        fields = '__all__'

class UserDataSerializer(serializers.Serializer):
    genres = GenreSerializer(many=True)
    books = BookSerializer(many=True)
    ratings = CustomerRatingSerializer(many=True)