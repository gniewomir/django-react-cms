FROM python:3.6.5-stretch
ARG unbuffered
ARG uncached
ARG environment
ENV PATH /root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=$unbuffered
ENV PYTHONDONTWRITEBYTECODE=$uncached
ENV DEBUG=true
ENV ENVIRONMENT=$environment
WORKDIR /home/django/app
COPY . /home/django/app
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r requirements.txt \
    && CMS_DATABASE_URL=none CMS_DB_NAME=none CMS_DB_USER=none CMS_DB_PASS=none CMS_DB_SERVICE=none CMS_DB_PORT=none SECRET_KEY=none \
    /usr/local/bin/python /home/django/app/manage.py collectstatic --noinput
CMD ["/root/.local/bin/gunicorn","settings.wsgi:application","-w 2", "-b :8000"]