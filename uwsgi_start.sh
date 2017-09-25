uwsgi --http :4000 --wsgi-file uwsgi.py --pidfile uwsgi.pid --daemonize uwsgi.log --master --processes 1 --threads 1
