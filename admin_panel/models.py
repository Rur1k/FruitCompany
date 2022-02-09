from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=16)
    count = models.IntegerField()
    price_buy = models.FloatField()
    price_sell = models.FloatField()

    def __str__(self):
        return self.name


class Wallet(models.Model):
    money = models.FloatField(default=0)
