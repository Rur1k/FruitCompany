from django.urls import path
from .views import FruitView, main_page

urlpatterns = [
    # path('', FruitView.as_view()),
    path('', main_page)
]
