import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from FruitCompany.celery import app
from celery import shared_task

from .models import Fruit, Wallet

channel_layer = get_channel_layer()

@app.task
def replenishment_warehouse():
    print('Работает таска')


# Пополнение склада
@shared_task
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
        result = f'SUCCESS: Склад пополнен на {add} {obj.name}! Заплачено:{add * obj.price_buy}'

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
            'count_fruit': obj.count,
            'wallet_money': wallet.money
        }
    )


# Продажа фруктов
@app.task
def sell_fruit(fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    count_sell = random.randrange(start, stop, step)
    if count_sell > obj.count:
        result = f'ERROR: Невозможно продать {count_sell} {obj.name}! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        money = wallet.money + count_sell*obj.price_sell
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        result = f'SUCCESS: С склада продано {count_sell} {obj.name}! Заработано: {count_sell * obj.price_sell}'

    async_to_sync(channel_layer.group_send)(
        'warehouse',
        {
            'type': 'log',
            'log': result,
            'fruit_id': fruit_id,
            'count_fruit': obj.count,
            'wallet_money': wallet.money
        }
    )
