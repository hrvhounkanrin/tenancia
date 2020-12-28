import os
from django.conf import settings
from django.apps import apps
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meslimmo.settings')

app = Celery('meslimmo')
# app = Celery('drfjwtauthapi',backend='amqp://localhost',broker='amqp://localhost')
# app = Celery('drfjwtauthapi', backend='rpc://', broker='amqp://jimmy:jimmy123@localhost/jimmy_vhost')
app.config_from_object('django.conf:settings')
# app.config_from_object(settings)
# app.autodiscover_tasks(settings.INSTALLED_APPS)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
