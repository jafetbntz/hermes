FROM python:3.8.5-slim

COPY ./src /srv/snapshot_service
COPY ./requirements.txt /srv/snapshot_service/requirements.txt

WORKDIR /srv/snapshot_service

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install -r requirements.txt --src /usr/local/src
RUN pip install uwsgi

COPY nginx/nginx.conf /etc/nginx

RUN chmod +x ./start.sh

RUN mkdir -p /var/www/html/pictures
RUN chmod 7555 /var/www/html/pictures

EXPOSE 80

CMD ["./start.sh"]
