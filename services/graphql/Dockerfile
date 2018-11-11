FROM node:10.10.0 as builder

ARG environment
ARG name

ENV SERVICE=$name
ENV ENVIRONMENT=$environment
ENV SOURCE=./services/$SERVICE
ENV DESTINATION=/dist

WORKDIR $DESTINATION
COPY ./shared/node/ $DESTINATION/lib
COPY $SOURCE/package*.json $DESTINATION/
RUN npm ci
COPY $SOURCE/src/ ./src
COPY $SOURCE/.env \
     $SOURCE/docker-entrypoint.sh \
     $SOURCE/index.js \
     ./

ENTRYPOINT ["bash", "/dist/docker-entrypoint.sh"]