from config.settings import celery_app
from ..utils import create_target_updates_by_percents


@celery_app.task
def create_target_updates_by_percents_task():
    create_target_updates_by_percents()
