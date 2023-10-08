from django.urls import path

from src.api.user_auth.views import *

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='api_login'),
    path('register/', UserRegisterAPIView.as_view(), name='api_register'),
    path('profile/', UserProfileGetUpdateAPIView.as_view(), name='api_profile'),
]
