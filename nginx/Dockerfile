FROM nginx:alpine

RUN apk add --no-cache gettext

COPY entrypoint.sh /entrypoint.sh
COPY nginx.conf.template /etc/nginx/nginx.conf.template

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
