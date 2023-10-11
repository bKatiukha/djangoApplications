from rest_framework import serializers
from src.chat.models import Room, Message


class RoomSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Room
        fields = ['name', 'created_at', 'uuid', 'created_by']


class MessageSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Message
        fields = ['created_by', 'created_at', 'message']


class RoomDetailsSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username')
    messages = MessageSerializer(many=True)

    class Meta:
        model = Room
        fields = ['name', 'created_at', 'uuid', 'created_by', 'messages']


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name']
