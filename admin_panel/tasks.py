import random
from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from FruitCompany.celery import app
from celery import shared_task

from .models import Fruit, Wallet

channel_layer = get_channel_layer()


# Кошелек
@app.task(one_options={'fail': False})
def wallet_money():
    wallet = Wallet.objects.get(pk=1)

    async_to_sync(channel_layer.group_send)(
        'wallet',
        {
            'type': 'wallet_update',
            'res': wallet.money,
        }
    )


@app.task(one_options={'fail': False})
def add_wallet_money(money_sum):
    wallet = Wallet.objects.get(pk=1)
    new_sum = wallet.money + float(money_sum)
    Wallet.objects.filter(pk=1).update(money=new_sum)

    async_to_sync(channel_layer.group_send)(
        'wallet',
        {
            'type': 'wallet_update',
            'res': new_sum,
        }
    )


@app.task(one_options={'fail': False})
def minus_wallet_money(money_sum):
    wallet = Wallet.objects.get(pk=1)
    if wallet.money >= float(money_sum):
        new_sum = wallet.money - float(money_sum)
        Wallet.objects.filter(pk=1).update(money=new_sum)
    else:
        new_sum = wallet.money

    async_to_sync(channel_layer.group_send)(
        'wallet',
        {
            'type': 'wallet_update',
            'res': new_sum,
        }
    )


@app.task(one_options={'fail': False})
def fruit_count(fruit_id):
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

@app.task(one_options={'fail': False})
def manual_buy_fruit(fruit_id, add):
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
        result = f'SUCCESS: Склад пополнен на {add} {obj.name}! Заплачено: {add * obj.price_buy} usd - пользователь'

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )


# Продажа фруктов

@app.task(one_options={'fail': False})
def manual_sell_fruit(fruit_id, count_sell):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    count_sell = int(count_sell)

    if count_sell > obj.count:
        result = f'ERROR: Невозможно продать {count_sell} {obj.name}! Недостаток на складе. - пользователь'
    else:
        count = obj.count - count_sell
        money = wallet.money + count_sell * obj.price_sell
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'SUCCESS: Продано {count_sell} {obj.name}! Заработано: {count_sell * obj.price_sell} usd - пользователь'

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

@app.task(one_options={'fail': False})
def replenishment_warehouse_fruit(fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    add = random.randrange(start, stop, step)
    if (add * obj.price_buy) > wallet.money:
        result = f'ERRORS: Не достаточно денег для закупки {add} {obj.name}!'
    else:
        count = obj.count + add
        money = wallet.money - (add * obj.price_buy)
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'SUCCESS: Склад пополнен на {add} {obj.name}! Заплачено:{add * obj.price_buy} usd'

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )


# Продажа фруктов
@app.task(one_options={'fail': False})
def sell_fruit(fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    count_sell = random.randrange(start, stop, step)
    if count_sell > obj.count:
        result = f'ERROR: Невозможно продать {count_sell} {obj.name}! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        money = wallet.money + count_sell * obj.price_sell
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'SUCCESS: Продано {count_sell} {obj.name}! Заработано: {count_sell * obj.price_sell} usd '

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
        }
    )
