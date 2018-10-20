FROM python:3.6.5-stretch
ARG environment
ENV ENVIRONMENT=$environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH /root/.local/bin:$PATH
WORKDIR /home/django/app
COPY ./services/cms/ /home/django/app
COPY ./shared/ /home/django/app/shared
RUN pip install --user --no-cache-dir -r requirements.txt
ENTRYPOINT ["bash", "/home/django/app/startup.sh"]