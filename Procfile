web: gunicorn majibu.wsgi --log-file -
worker: celery -A majibu worker -l info
beat: celery -A majibu beat -l info
