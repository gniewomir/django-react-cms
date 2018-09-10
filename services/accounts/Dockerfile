FROM python:3.6.5-stretch
ARG environment
ENV ENVIRONMENT=$environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH /root/.local/bin:$PATH
WORKDIR /home/django/app
COPY . /home/django/app
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt \
    && ACCOUNTS_DATABASE_URL=none ACCOUNTS_DB_NAME=none ACCOUNTS_DB_USER=none ACCOUNTS_DB_PASS=none ACCOUNTS_DB_SERVICE=none ACCOUNTS_DB_PORT=none SECRET_KEY=none \
    /usr/local/bin/python /home/django/app/manage.py collectstatic --noinput
CMD ["/root/.local/bin/gunicorn","settings.wsgi:application","-w 2", "-b :8000"]