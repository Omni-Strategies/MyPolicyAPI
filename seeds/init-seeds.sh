#!/bin/sh
set -e

for f in /docker-entrypoint-initdb.d/seeds/*.sql; do
  echo "Running $f"
  psql -v ON_ERROR_STOP=1 \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    -f "$f"

done
