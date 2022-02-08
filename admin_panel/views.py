from django.shortcuts import render
from django.views.generic import ListView

from .models import Fruit
from .forms import FruitForm


class FruitView(ListView):
    model = Fruit
    template_name = 'fruit.html'
