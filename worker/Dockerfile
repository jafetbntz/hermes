FROM python:3.8.5-slim

COPY ./src /srv/books_app
COPY ./requirements.txt /srv/books_app/requirements.txt

WORKDIR /srv/books_app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install -r requirements.txt --src /usr/local/src
RUN pip install uwsgi

COPY nginx/nginx.conf /etc/nginx

RUN chmod +x ./start.sh

EXPOSE 80

CMD ["./start.sh"]
