web: gunicorn lets_stonk_about_it.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate