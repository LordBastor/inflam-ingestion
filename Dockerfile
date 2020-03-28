FROM python:3.7-alpine

COPY ./requirements.txt /requirements.txt
COPY ./.env /.env

WORKDIR /

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
