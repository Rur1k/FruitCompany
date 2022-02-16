import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from .models import Fruit, Wallet, ChatMessage
from .forms import LoginForm
from .tasks import parserJoke


def login_user(request):
    if request.user.is_authenticated:
        return redirect('room')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = User.objects.filter(email=cd['email']).first()
            if username is None:
                return redirect('login')

            user = authenticate(username=username, password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('room')
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'admin_panel/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def index(request):
    return render(request, 'admin_panel/index.html')


def warehouse(request):
    fruits = Fruit.objects.all()
    room_name = 'warehouse'

    message_list = ChatMessage.objects.all()[:40]
    messages = []
    for obj in message_list:
        messages.insert(0, obj)

    data = {
        'object_list': fruits,
        'wallet': Wallet.objects.get(pk=1),
        'room_name_json': mark_safe(json.dumps(room_name)),
        'messages': messages
    }
    return render(request, 'admin_panel/warehouse.html', data)
