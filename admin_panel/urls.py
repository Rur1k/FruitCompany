from django.urls import path
from .views import index, warehouse, login_user, logout_user, ajax_select_log

urlpatterns = [
    path('', warehouse, name='room'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('ajax/', ajax_select_log, name='select_log')
]
