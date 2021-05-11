import os
from django.conf import settings
from celery.schedules import crontab
from django.apps import apps
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meslimmo.settings')
from setup import main as project_setup_main
project_setup_main()
app = Celery('meslimmo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


app.conf.beat_schedule = {
    'trigger_echeancier': {
        'task': 'tasks.get_contrat_en_cours',
        'schedule': crontab(minute='*/2')
    },
}
