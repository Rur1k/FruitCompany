from django.urls import path
from .views import index, warehouse

urlpatterns = [
    path('', index, name='index'),
    path('<str:room_name>/', warehouse, name='room')
]
