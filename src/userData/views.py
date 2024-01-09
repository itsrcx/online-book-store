from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Genre, Book, CustomerRating
from .serializers import GenreSerializer, BookSerializer, CustomerRatingSerializer


class UserDataAPIView(APIView):
    queryset = Book.objects.all()
    def get(self, request, *args, **kwargs):
        user = self.request.user  # Assuming you have authentication set up
        genres = Genre.objects.filter(book__customer_rating__user=user).distinct()
        books = Book.objects.filter(customer_rating__user=user).distinct()
        ratings = CustomerRating.objects.filter(user=user)

        genre_serializer = GenreSerializer(genres, many=True)
        book_serializer = BookSerializer(books, many=True)
        rating_serializer = CustomerRatingSerializer(ratings, many=True)

        data = {
            'genres': genre_serializer.data,
            'books': book_serializer.data,
            'ratings': rating_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
