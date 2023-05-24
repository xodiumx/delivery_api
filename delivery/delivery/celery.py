from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery.settings')

app = Celery('delivery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-tokens': {
        'task': 'api.tasks.update_locations_of_all_cars',
        'schedule': crontab(minute='*/3'),
    },
}
app.conf.timezone = 'UTC'