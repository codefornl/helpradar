FROM python:3.8.2-buster

WORKDIR /usr/helpradar
RUN apt-get update && apt-get install -yq cron

COPY src .
COPY docker-crontab /etc/cron.d/helpradar
RUN pip install -r requirements.txt

CMD ["cron", "-f"]