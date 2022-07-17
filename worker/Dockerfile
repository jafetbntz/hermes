FROM python:3.8.5-slim

COPY ./src /srv/hermes_worker
COPY ./requirements.txt /srv/hermes_worker/requirements.txt

WORKDIR /srv/hermes_worker

RUN pip install -r requirements.txt --src /usr/local/src

CMD ["python", "-u", "./worker.py"]
