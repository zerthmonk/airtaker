#!/usr/bin/env bash

TARGET_DIR=./backend/bemeta/core/static

# fresh Vue build from scratch
docker-compose run --rm front-builder sh -c "npm run build" &&
mkdir -p $TARGET_DIR &&
rm -rf $TARGET_DIR/*
cp -r ./frontend/dist/* $TARGET_DIR/ &&

echo 'build completed, files now in' $TARGET_DIR
