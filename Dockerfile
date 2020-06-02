FROM python:3.8.2-buster

ENV DB_HOST postgresql
ENV DB_USER postgres
ENV DB_PASSWORD secret
ENV DB_NAME postgres

WORKDIR /usr/helpradar
RUN apt-get update && apt-get install -yq cron

COPY src .
COPY docker-crontab /etc/cron.d/helpradar
RUN pip install -r requirements.txt

CMD ["cron", "-f"]