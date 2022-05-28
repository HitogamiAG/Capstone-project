from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse


# Create your views here.


def messenger(request):
    return render(request, 'messenger/index.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(room=room)
    return render(request, 'messenger/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    room_name = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(room=room_name).exists():
        return redirect(f'/{room_name}/?username={username}')
    else:
        new_room = Room.objects.create(room=room_name)
        new_room.save()
        return redirect(f'/{room_name}/?username={username}')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    new_message = Message.objects.create(content=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(room=room)

    messages = Message.objects.filter(room=room_details.id)

    return JsonResponse({"messages": list(messages.values())})

