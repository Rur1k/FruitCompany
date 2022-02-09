# Встроенные импорты.
import json

# Импорты сторонних библиотек.
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncWebsocketConsumer

# Импорты Django.
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

# Локальные импорты.
from FruitCompany.admin_panel.models import Fruit
from FruitCompany.admin_panel.utils import get_count_apple


class LiveScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       self.room_name = self.scope['url_route']['kwargs']['game_id']
       self.room_group_name = f'Game_{self.room_name}'

       if self.scope['user'] == AnonymousUser():
           raise DenyConnection("Такого пользователя не существует")

       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       )

       # If invalid game id then deny the connection.
       try:
            self.game = Fruit.objects.get(pk=self.room_name)
       except ObjectDoesNotExist:
            raise DenyConnection("Неверный ID игры")

       await self.accept()

    async def receive(self, text_data):
       game_city = json.loads(text_data).get('game_city')

       await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'live_score',
                'game_id': self.room_name,
                'game_city': game_city
            }
        )

    async def live_score(self, event):
        city = event['game_city']
        # Вспомогательная функция, получающая счет игры из БД.
        await self.send(text_data=json.dumps({
                'score': get_live_score_for_game(self.game, city)
            }))

    async def websocket_disconnect(self, message):
        pass