
release: python manage.py migrate
web: python manage.py migrate --fake-initial && python manage.py migrate --run-syncdb && gunicorn portfolio_site.wsgi --log-file -