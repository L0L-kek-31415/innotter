FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

RUN pip install pipenv

RUN apt-get update \
    && apt-get install -yyq netcat


COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system --ignore-pipfile

COPY . .

RUN ["chmod", "+x", "./entrypoint.sh"]
RUN ["chmod", "+x", "./celery-entrypoint.sh"]

