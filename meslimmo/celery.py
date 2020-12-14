import os
from django.conf import  settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meslimmo.settings')

app = Celery('meslimmo')
# app = Celery('drfjwtauthapi',backend='amqp://localhost',broker='amqp://localhost')
# app = Celery('drfjwtauthapi', backend='rpc://', broker='amqp://jimmy:jimmy123@localhost/jimmy_vhost')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
