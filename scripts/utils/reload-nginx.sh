#!/bin/sh

set -e;

# reload conf in nginx container
docker exec -it $(basename $PWD)_nginx_1 nginx -s reload

# for example, if certbot has renewed certificates