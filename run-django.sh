#!/usr/bin/env bash

RUN="pipenv run python ./backend/bemeta/manage.py"
#export DJANGO_LISTEN=$(grep DJANGO_LISTEN .env | cut -f2 -d "=")

$RUN collectstatic --no-input --clear &&
yes | $RUN makemigrations &&
yes yes | $RUN migrate &&
$RUN runserver 0.0.0.0:8000
