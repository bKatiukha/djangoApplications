from django.urls import path
from src.api.chat.views import *

urlpatterns = [
    path('rooms/', RoomListAPIView.as_view(), name='rooms'),
    path('user_rooms/', UserRoomsAPIView.as_view(), name='user_rooms'),
    path('create_room/', RoomCreateAPIView.as_view(), name='create_room'),
]
