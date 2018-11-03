FROM nginx:1.15.5-alpine

ARG environment

ENV ENVIRONMENT=$environment

RUN rm /etc/nginx/conf.d/default.conf && \
    rm /etc/nginx/nginx.conf
ADD ./services/nginx/conf.d.$ENVIRONMENT/ /etc/nginx/conf.d
ADD ./services/nginx/cert.$ENVIRONMENT/ /etc/nginx/cert
ADD ./services/nginx/nginx.conf /etc/nginx/nginx.conf
