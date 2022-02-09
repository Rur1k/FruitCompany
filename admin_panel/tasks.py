import random
from FruitCompany.celery import app

from .models import Fruit, Wallet


@app.task
def replenishment_warehouse():
    print('Работает таска')


# Пополнение склада
# @app.task
# def replenishment_warehouse_apple_wallet():
#     obj = Fruit.objects.get(pk=1)
#     wallet = Wallet.objects.get(pk=1)
#
#     add = random.randrange(10)
#     if (add * obj.price_buy) > wallet.money:
#         return f'ERRORS: Не достаточно денег для закупки яблок!'
#     else:
#         count = obj.count + add
#         money = wallet.money - (add * obj.price_buy)
#         Fruit.objects.filter(pk=1).update(count=count)
#         Wallet.objects.filter(pk=1).update(money=money)
#         return f'SUCCESS: Склад пополнен на {add} яблок! Заплачено:{add * obj.price_buy}'


@app.task
def replenishment_warehouse_apple():
    obj = Fruit.objects.get(pk=1)
    add = random.randrange(10)
    count = obj.count + add
    Fruit.objects.filter(pk=1).update(count=count)
    return f'SUCCESS: Склад пополнен на {add} яблок!'

@app.task
def replenishment_warehouse_banana():
    obj = Fruit.objects.get(pk=2)
    add = random.randrange(10, 20, 1)
    count = obj.count + add
    Fruit.objects.filter(pk=2).update(count=count)
    return f'SUCCESS: Склад пополнен на {add} бананов!'


@app.task
def replenishment_warehouse_pineapple():
    obj = Fruit.objects.get(pk=3)
    add = random.randrange(10)
    count = obj.count + add
    Fruit.objects.filter(pk=3).update(count=count)
    return f'SUCCESS: Склад пополнен на {add} ананасов!'


@app.task
def replenishment_warehouse_peach():
    obj = Fruit.objects.get(pk=4)
    add = random.randrange(5, 15, 1)
    count = obj.count + add
    Fruit.objects.filter(pk=4).update(count=count)
    return f'SUCCESS: Склад пополнен на {add} персиков!'


# Расхищение склада
# @app.task
# def sell_apple_wallet():
#     obj = Fruit.objects.get(pk=1)
#     wallet = Wallet.objects.get(pk=1)
#
#     count_sell = random.randrange(10)
#     if count_sell > obj.count:
#         return f'ERROR: Невозможно продать {count_sell} яблок! Недостаток на складе.'
#     else:
#         count = obj.count - count_sell
#         money = wallet.money + count_sell*obj.price_sell
#         Fruit.objects.filter(pk=1).update(count=count)
#         Wallet.objects.filter(pk=1).update(money=money)
#         return f'SUCCESS: С склада продано {count_sell} яблок! Заработано: {count_sell*obj.price_sell}'

@app.task
def sell_apple():
    obj = Fruit.objects.get(pk=1)
    count_sell = random.randrange(10)
    if count_sell > obj.count:
        return f'ERROR: Невозможно продать {count_sell} яблок! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        Fruit.objects.filter(pk=1).update(count=count)
        return f'SUCCESS: С склада продано {count_sell} яблок! Заработано: {count_sell*obj.price_sell}'


@app.task
def sell_banana():
    obj = Fruit.objects.get(pk=2)
    count_sell = random.randrange(30)
    if count_sell > obj.count:
        return f'ERROR: Невозможно продать {count_sell} бананов! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        Fruit.objects.filter(pk=2).update(count=count)
        return f'SUCCESS: С склада продано {count_sell} бананов! Заработано: {count_sell*obj.price_sell}'


@app.task
def sell_pineapple():
    obj = Fruit.objects.get(pk=3)
    count_sell = random.randrange(10)
    if count_sell > obj.count:
        return f'ERROR: Невозможно продать {count_sell} ананасов! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        Fruit.objects.filter(pk=3).update(count=count)
        return f'SUCCESS: С склада продано {count_sell} ананасов! Заработано: {count_sell*obj.price_sell}'


@app.task
def sell_peach():
    obj = Fruit.objects.get(pk=4)
    count_sell = random.randrange(20)
    if count_sell > obj.count:
        return f'ERROR: Невозможно продать {count_sell} персиков! Недостаток на складе.'
    else:
        count = obj.count - count_sell
        Fruit.objects.filter(pk=5).update(count=count)
        return f'SUCCESS: С склада продано {count_sell} персиков! Заработано: {count_sell*obj.price_sell}'

