#!/usr/bin/env bash

RUN="pipenv run python ./backend/bemeta/manage.py"
export DJANGO_LISTEN=$(grep LISTEN .env | cut -f2 -d "=")

$RUN wait_for_db &&
$RUN collectstatic --no-input --clear &&
yes | $RUN makemigrations &&
yes yes | $RUN migrate &&
$RUN runserver $DJANGO_LISTEN
