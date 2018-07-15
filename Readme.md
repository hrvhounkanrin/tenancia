=====
meslimmo
=====


meslimmo contains api for mmesley immo application.

Detailed documentation is in the "docs" directory.

Build chronos_models as reusable application
-----------
1. Run `python3 setup.py sdist`
2. Run `pip3 install --user dist/chronos_models-1.0.0.tar.gz`

or run
pip3 install --editable /path/to/meslimmo()

Note= for more informations read those links
- https://docs.djangoproject.com/en/1.8/intro/reusable-apps/ or
- https://stackoverflow.com/questions/30743720/how-to-develop-include-a-django-custom-reusable-app-in-a-new-project-are-there

Quick start
-----------

1. Add "mimmob_data_service" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'meslimmo',
    )


2. Run `python3 manage.py migrate` to create the polls models.

NOTE:
 1- In manage.py and meslimmo/wsgi.py, replace :
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meslimmo.settings") by
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meslimmo.settings.development")

 2- duplivate env file and rename the second .env and update information on .env file(But don't  
 update DJANGO_SETTINGS_MODULE and don't push .env file)
