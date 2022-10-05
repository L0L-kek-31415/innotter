FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -yyq netcat

WORKDIR /usr/src/app/

RUN pip install pipenv && pipenv install --deploy --system --ignore-pipfile
COPY Pipfile Pipfile.lock ./

COPY . /usr/src/app

RUN ["chmod", "+x", "./entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]