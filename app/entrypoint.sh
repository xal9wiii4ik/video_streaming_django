#!/bin/sh

if [ "$DATABASE" = "postgres" ]
  then
    echo "Waiting for psql"

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Psql started"
fi

python app/manage.py migrate
python app/manage.py collectstatic --noinput
python app/manage.py runserver 0.0.0.0:8000
