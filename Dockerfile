FROM python:3.9.1-slim as base
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --no-install-recommends -y curl build-essential

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r ./app/requirements.txt

RUN chmod u+x ./app/entrypoint.sh

FROM base as dev
RUN apt-get install -y git
RUN pip3 install pre-commit mypy flake8

FROM base as prod
