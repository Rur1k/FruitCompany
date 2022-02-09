from django.shortcuts import render
from django.views.generic import ListView

from .models import Fruit, Wallet
from .forms import FruitForm
from .tasks import replenishment_warehouse


class FruitView(ListView):
    model = Fruit
    template_name = 'fruit.html'

    def get_queryset(self):
        queryset = self.model.objects.all()

        # replenishment_warehouse.delay()

        return queryset


def main_page(request):
    fruits = Fruit.objects.all()

    data = {
        'object_list': fruits,
        'wallet': Wallet.objects.get(pk=1)
    }
    return render(request, 'fruit.html', data)

