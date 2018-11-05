import datetime
from meslimmo.settings.commons import *
import os

DATABASES = {
    'default': {
        'ENGINE': os.environ['DATABASE_ENGINE'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],   # Or an IP Address that your DB is hosted on
        'PORT': os.environ['DATABASE_PORT'],
    }
}