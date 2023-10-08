from rest_framework import serializers
from src.chat.models import Room


class RoomSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Room
        fields = ['name', 'created_at', 'uuid', 'created_by']


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']
