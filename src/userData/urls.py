from django.urls import path
from .views import UserDataAPIView

urlpatterns = [
    path('userData/', UserDataAPIView.as_view(), name='user-data'),
]