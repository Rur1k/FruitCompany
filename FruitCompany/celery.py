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
        'task': 'admin_panel.tasks.replenishment_warehouse_apple',
        'schedule': timedelta(seconds=6),
    },
    'add-banana-every-9-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_banana',
        'schedule': timedelta(seconds=9),
    },
    'add-pineapple-every-12-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_pineapple',
        'schedule': timedelta(seconds=12),
    },
    'add-peach-every-15-second': {
        'task': 'admin_panel.tasks.replenishment_warehouse_peach',
        'schedule': timedelta(seconds=15),
    },
    'sell-apple-every-15-second': {
        'task': 'admin_panel.tasks.sell_apple',
        'schedule': timedelta(seconds=15),
    },
    'sell-banana-every-12-second': {
        'task': 'admin_panel.tasks.sell_banana',
        'schedule': timedelta(seconds=12),
    },
    'sell-pineapple-every-9-second': {
        'task': 'admin_panel.tasks.sell_pineapple',
        'schedule': timedelta(seconds=9),
    },
    'sell-peach-every-9-second': {
        'task': 'admin_panel.tasks.sell_peach',
        'schedule': timedelta(seconds=6),
    },
}

# app.conf.beat_schedule = {
#     'add-apple-every-6-second': {
#         'task': 'admin_panel.tasks.replenishment_warehouse_apple_wallet',
#         'schedule': timedelta(seconds=6),
#     },
#     'sell-apple-every-15-second': {
#         'task': 'admin_panel.tasks.sell_apple_wallet',
#         'schedule': timedelta(seconds=15),
#     },
# }


