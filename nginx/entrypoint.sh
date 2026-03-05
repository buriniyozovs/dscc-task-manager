#!/bin/sh
set -e
envsubst '${SSL_DOMAIN}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf
exec nginx -g 'daemon off;'
