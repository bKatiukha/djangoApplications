from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from src.chat.models import Room, Message


@login_required
def chat(request):
    all_chats = Room.objects.all()
    context = {
        'title': 'chat',
        'all_chats': all_chats,
    }
    return render(request, 'chat/chat.html',  context=context)


@login_required
def chat_uuid(request, uuid):
    room = Room.objects.get(uuid=uuid)
    messages = Message.objects.filter(room=room)
    context = {
        'title': 'chat uuid',
        'room': room,
        'messages': messages,
    }
    return render(request, 'chat/chat_uuid.html', context=context)
