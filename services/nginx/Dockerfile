FROM nginx:1.15.5-alpine
RUN rm /etc/nginx/conf.d/default.conf && \
    rm /etc/nginx/nginx.conf
ADD ./services/nginx/conf.d/ /etc/nginx/conf.d
ADD ./services/nginx/cert/ /etc/nginx/cert
ADD ./services/nginx/nginx.conf /etc/nginx/nginx.conf
