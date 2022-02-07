web: gunicorn lets_stonk_about_it.wsgi --log-file - --log-level debug
heroku ps:scale web=1
manage.py migrate