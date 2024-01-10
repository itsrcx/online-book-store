from django.urls import path
from .views import AllUserDataAPIView

urlpatterns = [
    path('userData/', AllUserDataAPIView.as_view(), name='user-data'),
]