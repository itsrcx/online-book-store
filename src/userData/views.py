from rest_framework.views import APIView
from rest_framework.response import Response
from books.models import CustomerRating
from .serializers import UserDataSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class AllUserDataAPIView(APIView):
    def get(self, request, *args, **kwargs):
        all_users = User.objects.all()
        user_data = []

        for user in all_users:
            rated_books = CustomerRating.objects.filter(user=user).select_related('book__genre')
            serialized_data = UserDataSerializer({'user': user, 'rated_books': rated_books}, context={'request': request})
            user_data.append(serialized_data.data)

        return Response(user_data)
    
    # permission_classes = [IsAuthenticated]