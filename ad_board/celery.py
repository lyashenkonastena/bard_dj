import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_board.settings')

app = Celery('ad_board')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_blog_digest_weekly': {
        'task': 'notifier.tasks.send_blog_digest',
        'schedule': crontab(day_of_week="monday",
                            hour="12",
                            minute="00"),
    },
}

app.autodiscover_tasks()
