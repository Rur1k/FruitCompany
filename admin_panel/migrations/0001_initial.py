# Generated by Django 3.2.4 on 2022-02-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('count', models.IntegerField()),
                ('price_buy', models.FloatField()),
                ('price_sell', models.FloatField()),
            ],
        ),
    ]