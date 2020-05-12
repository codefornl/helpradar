FROM python:3.8.2-buster

WORKDIR /usr/helpradar

COPY src .

RUN pip install -r requirements.txt

CMD [ "./docker-entrypoint.sh" ]