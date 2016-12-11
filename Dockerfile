FROM nginx:stable-alpine
RUN apk update
RUN apk add python3
RUN python3.5 -m pip install websockets asyncio
COPY client /opt/snake_turnament/client
COPY server /opt/snake_turnament/server
COPY docker_content/entrypoint.sh /entrypoint.sh
COPY docker_content/nginx_default.conf /etc/nginx/conf.d/default.conf

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]
