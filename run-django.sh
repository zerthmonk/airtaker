#!/usr/bin/env bash

RUN="pipenv run python ./backend/bemeta/manage.py"
LISTEN="0.0.0.0:8000"

$RUN wait_for_db &&
$RUN collectstatic --no-input --clear &&
yes | $RUN makemigrations &&
yes yes | $RUN migrate &&
$RUN runserver $LISTEN
