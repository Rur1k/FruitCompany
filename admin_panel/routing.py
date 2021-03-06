from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/log/(?P<room_name>\w+)/$', consumers.TaskConsumer.as_asgi()),
    re_path(r'ws/wallet/(?P<room_name>\w+)/$', consumers.WalletConsumer.as_asgi()),
    re_path(r'ws/loop/(?P<room_name>\w+)/$', consumers.LoopConsumer.as_asgi()),
    re_path(r'ws/loopStatus/(?P<room_name>\w+)/$', consumers.LoopStatusConsumer.as_asgi()),
]
