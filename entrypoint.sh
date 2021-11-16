#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi
echo "Start migration"
# python manage.py flush --no-input
# python manage.py migrate
mkdir -p "LOGS"
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput
# make migrations
python manage.py makemigrations --no-input
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --no-input
python manage.py update_countries_plus
python manage.py load_autoname
python manage.py load_banks
python manage.py load_type_dependencies
python manage.py load_accessoires
if ["$DEBUG"==1]
then
  python manage.py loaddata user.json
  python manage.py loaddata client.json
  python manage.py loaddata proprietaire.json
fi


# celery -b rabbitmq -A meslimmo.celery worker --loglevel=debug
# Start server
echo "Starting server"
# python manage.py runserver 0.0.0.0:8000
exec "$@"
