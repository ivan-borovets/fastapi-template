#!/bin/sh
# The script is called from docker-compose.yaml
echo "APP_NAME is ${APP_NAME} (for docker-compose)"
echo
echo "SRC_DIR is ${SRC_DIR} (for docker-compose)"
echo "CONFIG_TOML is ${CONFIG_TOML} (for docker-compose)"
echo "PYPROJECT_TOML is ${PYPROJECT_TOML} (for docker-compose)"
echo "POETRY_LOCK is ${POETRY_LOCK} (for docker-compose)"
echo
echo "POSTGRES_USER is ${POSTGRES_USER} (for docker-compose)"
echo "POSTGRES_PASSWORD is ${POSTGRES_PASSWORD} (for docker-compose)"
echo "POSTGRES_DB is ${POSTGRES_DB} (for docker-compose)"
echo "POSTGRES_HOST is ${POSTGRES_HOST} (for docker-compose)"
echo "POSTGRES_PORT is ${POSTGRES_PORT} (for docker-compose)"
echo
echo "UVICORN_PORT is ${UVICORN_PORT} (for docker-compose)"

exit 0