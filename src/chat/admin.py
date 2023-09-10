from django.contrib import admin

from src.chat.models import Room, Message

admin.site.register(Room)
admin.site.register(Message)


