#!/bin/bash

# Conditional sourcing of .env file
if [[ -f ".env" ]]; then
  echo "env variables file found, sourcing..."
  source .env
else
  echo "env variables file not found, continuing without it."
fi

set -e
set -o nounset

export PATH=${PATH}:/src
export PYTHONPATH=/app/src

postgres_ready() {
    python << END
import sys

from psycopg2 import connect
from psycopg2.errors import OperationalError

try:
    connect(
        dbname="${DB_NAME}",
        user="${DB_USER}",
        password="${DB_PASSWORD}",
    )
except OperationalError:
    sys.exit(-1)
END
}
wait_other_containers() {
	until postgres_ready; do
		>&2 echo "Waiting for PostgreSQL to become available..."
		sleep 5
	done
	>&2 echo "PostgreSQL is available"

}


cd /app


case $1 in
	"bash")
		bash;;
	"server")
		wait_other_containers ;\

		echo "attempting migrations in debug mode" && \
		alembic -c src/chatcleaner/adapters/db/alembic.ini upgrade head && \

	 	if [ "$FASTAPI_DEBUG" = "true" ]; then
        uvicorn \
            src.chatcleaner.adapters.entrypoints.api.app:app \
            --reload \
			--host 0.0.0.0 \
			--proxy-headers \
			--forwarded-allow-ips * \
			--port 8088
		else
			uvicorn \
            	src.chatcleaner.adapters.entrypoints.api.app:app \
				--workers 2 \
				--host 0.0.0.0 \
				--proxy-headers \
			    --forwarded-allow-ips * \
				--port 8088
		fi
	;;
	"test")
		wait_other_containers ;\
	    pytest -svvv  -m "not slow and not integration" tests
		;;
	"test-last-failed")
		wait_other_containers ;\
	    TEST_RUN="TRUE" pytest -svvv --lf tests
		;;
	"test-current")
		wait_other_containers ;\
		pytest -m current --no-header
		;;
	"test-current-v")
		wait_other_containers ;\
		pytest -vv -m current --log-cli-level=DEBUG
		;;
	"test-domain")
		wait_other_containers ;\
		pytest tests/domain --log-cli-level=DEBUG
		;;
	"test-int")
		wait_other_containers ;\
		TEST_RUN="true" pytest tests/integrations --log-cli-level=DEBUG
		;;
	"test-repos")
		wait_other_containers ;\
		pytest tests/repositories --log-cli-level=DEBUG
		;;
	"test-services")
		wait_other_containers ;\
		pytest tests/services --log-cli-level=DEBUG
		;;
	"test-uows")
		wait_other_containers ;\
		pytest tests/unit_of_works --log-cli-level=DEBUG
		;;
	"test-cov")
		wait_other_containers ;\
		TEST_RUN="TRUE" pytest -svvv --cov-report html --cov=src tests
		;;
	"migrations")
		wait_other_containers ;\
		alembic -c src/chatcleaner/adapters/db/alembic.ini revision --autogenerate
		;;
	"migrate")
		wait_other_containers ;\
		alembic -c src/chatcleaner/adapters/db/alembic.ini upgrade head
		;;
	"*")
		exec "$@"
		;;
esac


