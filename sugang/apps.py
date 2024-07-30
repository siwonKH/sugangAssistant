from apscheduler.schedulers.background import BackgroundScheduler

from django.conf import settings
from django.apps import AppConfig


def remove_session():
    settings.SESSION_EXIST = False


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_session, 'interval', minutes=80)
    scheduler.start()


class SugangConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sugang'

    def ready(self):
        start_scheduler()
