#!/bin/bash

set -e
set -o nounset

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
	 	if [ "$FASTAPI_DEBUG" = "true" ]; then
        uvicorn \
            appname.main:app \
            --reload \
			--host 0.0.0.0 \
			--port 8000
		else
			uvicorn \
				appname.main:app \
				--workers 2 \
				--host 0.0.0.0 \
				--port 8000
		fi
	;;
	"test")
		wait_other_containers ;\
	    TEST_RUN="TRUE" pytest -svvv  tests
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
		pytest tests/integrations --log-cli-level=DEBUG
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
	"*")
		exec "$@"
		;;
esac


