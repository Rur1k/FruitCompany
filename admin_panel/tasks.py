import random
from time import sleep

import requests

from datetime import datetime

from django.contrib.auth.models import User

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from FruitCompany.celery import app
from celery import shared_task
from celery_singleton import Singleton


from bs4 import BeautifulSoup

from .models import Fruit, Wallet, ChatMessage, TaskTime

channel_layer = get_channel_layer()


@shared_task(bind=True, track_started=True, queue='JokerQueue')
def parserJoke(self, wait=10):
    url = 'https://tproger.ru/wp-content/plugins/citation-widget/get-quote.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    joke = soup.p.text

    print('Ожидание:' + str(wait))
    sleep(wait)
    print(joke)

    user = User.objects.get(username='joker')
    ChatMessage.objects.create(user=user, message=joke)

    async_to_sync(channel_layer.group_send)(
        'chat',
        {
            'type': 'chat_message',
            'message': joke,
            'user': user.pk
        }
    )

    parserJoke(wait=len(joke))


@shared_task(base=Singleton, bind=True, track_started=True, queue='DefaultQueue')
def chatHistory(self):
    message_list = ChatMessage.objects.all()[:40]
    messages = []
    for obj in message_list:
        messages.insert(0, obj)

    for mess in messages:
        async_to_sync(channel_layer.group_send)(
            'chat',
            {
                'type': 'chat_message',
                'message': mess.message,
                'user': mess.user.pk
            }
        )


@shared_task(base=Singleton, bind=True, track_started=True, queue='LoopQueue')
def loop(self):
    evil = 1
    for i in range(1, 10000000, 1):
        evil = evil + i
        evil = evil * i
        evil = evil / i
        evil = evil - i
        evil = evil + evil
        evil = evil * evil
        evil = evil / evil
        evil = evil - evil + 1

    fruit_1 = Fruit.objects.get(pk=1)
    fruit_2 = Fruit.objects.get(pk=2)
    fruit_3 = Fruit.objects.get(pk=3)
    fruit_4 = Fruit.objects.get(pk=4)

    TaskTime.objects.filter(task='loop').update(last_time=datetime.now())

    async_to_sync(channel_layer.group_send)(
        'loop',
        {
            'type': 'result_loop',
            'state': 'Склад обновлен.',
            'fruit_1': fruit_1.count,
            'fruit_2': fruit_2.count,
            'fruit_3': fruit_3.count,
            'fruit_4': fruit_4.count,
        }
    )


@shared_task(base=Singleton, bind=True, track_started=True, queue='DefaultQueue')
def get_status(self, run=False):
    if run:
        state = 'Running'
        message = 'Задача уже выполняеться'
    else:
        state = 'Start'
        message = 'Проверка склада начата!'

    async_to_sync(channel_layer.group_send)(
        'loopStatus',
        {
            'type': 'get_status_res',
            'state': state,
            'message': message,
        }
    )


# Кошелек
@shared_task(queue='DefaultQueue')
def wallet_money():
    wallet = Wallet.objects.get(pk=1)
    TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
    async_to_sync(channel_layer.group_send)(
        'wallet',
        {
            'type': 'wallet_update',
            'res': wallet.money,
        }
    )


@shared_task(bind=True, track_started=True, queue='DefaultQueue')
def add_wallet_money(self, money_sum):
    wallet = Wallet.objects.get(pk=1)
    new_sum = wallet.money + float(money_sum)
    Wallet.objects.filter(pk=1).update(money=new_sum)
    TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
    async_to_sync(channel_layer.group_send)(
        'wallet',
        {
            'type': 'wallet_update',
            'res': new_sum,
        }
    )


@shared_task(bind=True, track_started=True, queue='DefaultQueue')
def minus_wallet_money(self, money_sum):
    wallet = Wallet.objects.get(pk=1)
    if wallet.money >= float(money_sum):
        new_sum = wallet.money - float(money_sum)
        Wallet.objects.filter(pk=1).update(money=new_sum)
        TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
    else:
        new_sum = wallet.money

    async_to_sync(channel_layer.group_send)(
        'wallet',
        {
            'type': 'wallet_update',
            'res': new_sum,
        }
    )


@shared_task(bind=True, track_started=True)
def fruit_count(self, fruit_id):
    fruit = Fruit.objects.get(pk=fruit_id)

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'wallet_update',
            'res': fruit.count,
        }
    )


# Ручной запуск
# Пополнение склада

@shared_task(bind=True, track_started=True, queue='FruitQueue')
def manual_buy_fruit(self, fruit_id, add):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)
    add = int(add)
    if (add * obj.price_buy) > wallet.money:
        result = f'ERRORS: Не достаточно денег для закупки {add} {obj.name}!'
    else:
        count = obj.count + add
        money = wallet.money - (add * obj.price_buy)
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'{datetime.now()} SUCCESS: Склад пополнен на {add} {obj.name}! Заплачено: {add * obj.price_buy} usd - пользователь'
        TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
        TaskTime.objects.filter(task='buy_fruit').update(last_time=datetime.now())
    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )


# Продажа фруктов

@shared_task(bind=True, track_started=True, queue='FruitQueue')
def manual_sell_fruit(self, fruit_id, count_sell):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    count_sell = int(count_sell)

    if count_sell > obj.count:
        result = f'{datetime.now()} ERROR: Невозможно продать {count_sell} {obj.name}! Недостаток на складе. - пользователь'
    else:
        count = obj.count - count_sell
        money = wallet.money + count_sell * obj.price_sell
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'{datetime.now()} SUCCESS: Продано {count_sell} {obj.name}! Заработано: {count_sell * obj.price_sell} usd - пользователь'
        TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
        TaskTime.objects.filter(task='sell_fruit').update(last_time=datetime.now())

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )


# beats
# Пополнение склада

@shared_task(bind=True, track_started=True, queue='FruitQueue')
def replenishment_warehouse_fruit(self, fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    add = random.randrange(start, stop, step)
    if (add * obj.price_buy) > wallet.money:
        result = f'{datetime.now()} ERRORS: Не достаточно денег для закупки {add} {obj.name}!'
    else:
        count = obj.count + add
        money = wallet.money - (add * obj.price_buy)
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'{datetime.now()} SUCCESS: Склад пополнен на {add} {obj.name}! Заплачено:{add * obj.price_buy} usd'
        TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
        TaskTime.objects.filter(task='buy_fruit').update(last_time=datetime.now())

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )


# Продажа фруктов
@shared_task(bind=True, track_started=True, queue='FruitQueue')
def sell_fruit(self, fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    count_sell = random.randrange(start, stop, step)
    if count_sell > obj.count:
        result = f'{datetime.now()} ERROR: Невозможно продать {count_sell} {obj.name}! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        money = wallet.money + count_sell * obj.price_sell
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'{datetime.now()} SUCCESS: Продано {count_sell} {obj.name}! Заработано: {count_sell * obj.price_sell} usd '
        TaskTime.objects.filter(task='wallet').update(last_time=datetime.now())
        TaskTime.objects.filter(task='sell_fruit').update(last_time=datetime.now())

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )
