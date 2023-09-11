import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

from src.chat.models import Room, Message


def guid():
    def s4():
        return hex(int((1 + random.random()) * 0x10000))[3:]

    return f'{s4()}{s4()}-{s4()}-{s4()}-{s4()}-{s4()}{s4()}{s4()}'


@login_required
def chat(request):
    class ChatNameForm(forms.Form):
        name = forms.CharField(max_length=100)

    if request.method == 'POST':
        form = ChatNameForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            try:
                room = Room.objects.create(
                    **form.cleaned_data,
                    created_by=request.user,
                    uuid=guid()
                )
                return redirect(room.get_absolute_url())
            except:
                form.add_error(None, 'Form validation error')
    else:
        form = ChatNameForm()

    all_chats = Room.objects.select_related('created_by').all()
    my_chats = all_chats.filter(created_by=request.user.pk)

    context = {
        'title': 'chat',
        'all_chats': all_chats,
        'my_chats': my_chats,
        'create_chat_form': form
    }
    return render(request, 'chat/chat.html',  context=context)


@login_required
def chat_uuid(request, uuid):
    try:
        room = Room.objects.select_related('created_by').get(uuid=uuid)
        messages = Message.objects.select_related('created_by').filter(room=room)
        context = {
            'title': 'chat uuid',
            'room': room,
            'messages': messages,
        }
        return render(request, 'chat/chat_uuid.html', context=context)
    except Room.DoesNotExist:
        return redirect('chat')


