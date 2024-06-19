#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until psql "postgresql://myuser:mypassword@postgres:5432/mydatabase" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Run the Scrapy spider
scrapy crawl job_spider

# Run the query.py script
python query.py

tail -f /dev/null
