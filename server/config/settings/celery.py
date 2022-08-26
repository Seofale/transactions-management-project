import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("create_target_updates_by_percents")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'create-target-updates-every-day': {
        'task': 'apps.targets.tasks.create_target_updates_by_percents',
        'schedule': crontab(hour='*/24'),
    },
}
