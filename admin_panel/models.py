from django.db import models
from django.contrib.auth.models import User


class Fruit(models.Model):
    name = models.CharField(max_length=16)
    count = models.IntegerField()
    price_buy = models.FloatField()
    price_sell = models.FloatField()

    def __str__(self):
        return self.name


class Wallet(models.Model):
    money = models.FloatField(default=0)


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-pk']


class TaskTime(models.Model):
    task = models.CharField(max_length=64)
    last_time = models.DateTimeField()
    name = models.CharField(max_length=128, null=True, blank=True)
