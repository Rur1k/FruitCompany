import os

from celery import Celery
from celery.schedules import crontab

from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FruitCompany.settings')

app = Celery('FruitCompany')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-apple-every-6-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_fruit',
        'schedule': timedelta(seconds=6),
        'args': (1, 1, 10, 1),
    },
    'add-banana-every-9-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_fruit',
        'schedule': timedelta(seconds=9),
        'args': (2, 10, 20, 1),
    },
    'add-pineapple-every-12-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_fruit',
        'schedule': timedelta(seconds=12),
        'args': (3, 1, 10, 1),
    },
    'add-peach-every-15-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_fruit',
        'schedule': timedelta(seconds=15),
        'args': (4, 5, 15, 1),
    },
    'sell-apple-every-15-second': {
        'task': 'admin_panel.tasks.sell_fruit',
        'schedule': timedelta(seconds=15),
        'args': (1, 1, 10, 1),
    },
    'sell-banana-every-12-second': {
        'task': 'admin_panel.tasks.sell_fruit',
        'schedule': timedelta(seconds=12),
        'args': (2, 1, 30, 1),
    },
    'sell-pineapple-every-9-second': {
        'task': 'admin_panel.tasks.sell_fruit',
        'schedule': timedelta(seconds=9),
        'args': (3, 1, 10, 1),
    },
    'sell-peach-every-9-second': {
        'task': 'admin_panel.tasks.sell_fruit',
        'schedule': timedelta(seconds=6),
        'args': (4, 1, 20, 1),
    },
}



