FROM python:3.6.5-stretch

ARG environment
ARG name

ENV SERVICE=$name
ENV ENVIRONMENT=$environment
ENV SOURCE=./services/$SERVICE
ENV DESTINATION=/dist
ENV PATH /root/.local/bin:$PATH

ADD $SOURCE/requirements.txt $DESTINATION/
WORKDIR $DESTINATION/
RUN pip install --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt
COPY $SOURCE/.env \
     $SOURCE/docker-entrypoint.sh \
     $SOURCE/manage.py \
     $DESTINATION/
COPY $SOURCE/settings/ $DESTINATION/settings
COPY $SOURCE/apps/ $DESTINATION/apps
COPY $SOURCE/tests/ $DESTINATION/tests
COPY ./shared/ $DESTINATION/shared

ENTRYPOINT ["bash", "/dist/docker-entrypoint.sh"]