#!/usr/bin/env bash

if [ "$APP_ENV" != "dev" ]; then
  echo "APP_ENV=$APP_ENV"
  exit 0
fi

python main.py
echo "Есть жизнь"