from django.shortcuts import render
from django.views.generic import ListView

from .models import Fruit
from .forms import FruitForm
from .tasks import replenishment_warehouse


class FruitView(ListView):
    model = Fruit
    template_name = 'fruit.html'

    def get_queryset(self):
        queryset = self.model.objects.all()

        # replenishment_warehouse.delay()

        return queryset
