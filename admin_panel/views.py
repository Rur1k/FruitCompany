import json

from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import Fruit, Wallet



def index(request):
    return render(request, 'admin_panel/index.html')


def warehouse(request, room_name):
    fruits = Fruit.objects.all()

    data = {
        'object_list': fruits,
        'wallet': Wallet.objects.get(pk=1),
        'room_name_json': mark_safe(json.dumps(room_name))
    }
    return render(request, 'admin_panel/warehouse.html', data)

