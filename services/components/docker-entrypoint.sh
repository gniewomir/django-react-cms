#!/usr/bin/env bash
set -e
python manage.py collectstatic --clear --noinput
exec /root/.local/bin/gunicorn settings.wsgi:application \
     -w 2 \
     -b :8000
