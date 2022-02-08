from django.urls import path
from .views import FruitView

urlpatterns = [
    path('', FruitView.as_view()),
]
