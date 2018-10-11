FROM python:3.6.5-stretch
ARG environment
ENV ENVIRONMENT=$environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH /root/.local/bin:$PATH
WORKDIR /home/django/app
COPY . /home/django/app
RUN pip install --user --no-cache-dir -r requirements.txt
CMD ["/root/.local/bin/gunicorn","settings.wsgi:application","-w 2", "-b :8000"]