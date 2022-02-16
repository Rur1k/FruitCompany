from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .tasks import manual_buy_fruit, manual_sell_fruit, wallet_money, add_wallet_money, minus_wallet_money, loop, chatHistory
from .models import Wallet, ChatMessage
from django.contrib.auth.models import User

import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']

        user = User.objects.get(pk=user_id)
        ChatMessage.objects.create(user=user, message=message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user_id,
            }
        )

    def chat_message(self, event):
        message = event['message']
        user_id = event['user']

        user = User.objects.get(pk=user_id)

        self.send(text_data=json.dumps({
            'event': "Send",
            'message': message,
            'user': user.username
        }))


class TaskConsumer(WebsocketConsumer):
    strict_ordering = True

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'warehouse', self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'warehouse', self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        count = text_data_json['count']
        fruit_id = text_data_json['fruit_id']
        event = text_data_json['event']

        if event == 'buy':
            manual_buy_fruit.delay(fruit_id, count)
        else:
            manual_sell_fruit.delay(fruit_id, count)

    def log(self, event):
        log = event['log']
        fruit_id = event['fruit_id']
        wallet_money.delay()

        self.send(text_data=json.dumps({
            'log': log,
        }))


class WalletConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'wallet', self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'wallet', self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        money_sum = text_data_json['money_sum']
        event = text_data_json['event']

        if event == 'add':
            add_wallet_money.delay(money_sum)
        elif event == 'minus':
            minus_wallet_money.delay(money_sum)

    def wallet_update(self, event):
        money = event['res']
        self.send(text_data=json.dumps({
            'wallet_money': money,
        }))


class LoopConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'loop', self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'loop', self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        loop.delay()

    def result_loop(self, event):
        state = event['state']
        fruit_1 = event['fruit_1']
        fruit_2 = event['fruit_2']
        fruit_3 = event['fruit_3']
        fruit_4 = event['fruit_4']
        self.send(text_data=json.dumps({
            'res': state,
            'fruit_1': fruit_1,
            'fruit_2': fruit_2,
            'fruit_3': fruit_3,
            'fruit_4': fruit_4,

        }))
