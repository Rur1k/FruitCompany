import random
from FruitCompany.celery import app

from .models import Fruit, Wallet


@app.task
def replenishment_warehouse():
    print('Работает таска')


# Пополнение склада
@app.task
def replenishment_warehouse_fruit(fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    add = random.randrange(start, stop, step)
    if (add * obj.price_buy) > wallet.money:
        return f'ERRORS: Не достаточно денег для закупки {add} {obj.name}!'
    else:
        count = obj.count + add
        money = wallet.money - (add * obj.price_buy)
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        return f'SUCCESS: Склад пополнен на {add} {obj.name}! Заплачено:{add * obj.price_buy}'


# Продажа фруктов
@app.task
def sell_fruit(fruit_id, start=None, stop=None, step=None):
    obj = Fruit.objects.get(pk=fruit_id)
    wallet = Wallet.objects.get(pk=1)

    count_sell = random.randrange(start, stop, step)
    if count_sell > obj.count:
        return f'ERROR: Невозможно продать {count_sell} {obj.name}! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        money = wallet.money + count_sell*obj.price_sell
        Fruit.objects.filter(pk=fruit_id).update(count=count)
        Wallet.objects.filter(pk=1).update(money=money)
        return f'SUCCESS: С склада продано {count_sell} {obj.name}! Заработано: {count_sell * obj.price_sell}'
