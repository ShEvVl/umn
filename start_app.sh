#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c 'select 1'; do
    echo 'Waiting for database connection...'
    sleep 2
done

if [ ! -d /app/migrations ]; then
    flask db init && flask db migrate && flask db upgrade
else
    flask db migrate && flask db upgrade
fi

python run.py
