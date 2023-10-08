import random

from django.db.models import Q
from requests import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from src.api.chat.serializers import RoomSerializer, CreateRoomSerializer
from src.chat.models import Room


def guid():
    def s4():
        return hex(int((1 + random.random()) * 0x10000))[3:]

    return f'{s4()}{s4()}-{s4()}-{s4()}-{s4()}-{s4()}{s4()}{s4()}'


class UserRoomsAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(Q(created_by=user) | Q(messages__created_by=user)).distinct()


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]


class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer
    lookup_field = 'name'
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        serializer.save(name=name, created_by=self.request.user, uuid=guid())

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        room = self.queryset.get(name=response.data['name'])  # Assuming 'name' is unique
        room_serializer = RoomSerializer(room)
        response.data = room_serializer.data
        return response
