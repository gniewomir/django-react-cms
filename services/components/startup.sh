#!/usr/bin/env bash
python manage.py collectstatic --clear --noinput
/root/.local/bin/gunicorn settings.wsgi:application -w 2 -b :8000