#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started "


python manage.py collectstatic --no-input
python manage.py migrate --no-input

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('mariya.shinkareva', 'ms.shinkareva@yandex.ru', '12345678') if not User.objects.filter(username='mariya.shinkareva').exists() else 0" | python manage.py shell

uwsgi --http :8000 --chdir /opt/app --module config.wsgi:application

exec "$@"
