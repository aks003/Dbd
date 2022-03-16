web: gunicorn pg.wsgi --log-file - --log-level debug
heroku ps:scale web=1
manage.py migrate