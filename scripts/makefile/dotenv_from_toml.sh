#!/bin/bash
# The script is called from Makefile
if [[ ! -f config.toml ]]; then
  echo "Error: config.toml not found!"
  exit 1
fi

if [ "$1" != "docker" ] && [ "$1" != "local" ]; then
  echo "Usage: $0 [docker|local]"
  exit 1
fi

generate_env_var() {
  var_name=$1
  var_value=$(grep "$var_name" config.toml | sed 's/.*= *//;s/"//g')
  echo "${var_name}=${var_value}" >> .env
}

{
  echo "# This .env file was automatically generated."
  echo "# Do not edit directly."
  echo "# Make changes in config.toml instead."
  echo "# Then run \"make compose.create_dotenv.<choose env>\"."
  echo "# Last generated: $(date -u)"
} > .env

if [ "$1" = "docker" ]; then
  echo "IS_DOCKER=true" >> .env
else
  echo "IS_DOCKER=false" >> .env
fi
#
generate_env_var APP_NAME
#
generate_env_var SRC_DIR
generate_env_var CONFIG_TOML
generate_env_var PYPROJECT_TOML
generate_env_var POETRY_LOCK
#
generate_env_var POSTGRES_USER
generate_env_var POSTGRES_PASSWORD
generate_env_var POSTGRES_DB
if [ "$1" = "docker" ]; then
  generate_env_var POSTGRES_HOST
else
  echo "POSTGRES_HOST=localhost" >> .env
fi
generate_env_var POSTGRES_PORT
#
generate_env_var UVICORN_PORT

echo "The .env file has been generated successfully."
echo "Find .env in the directory with config.toml."
echo
echo "Contents of .env:"
cat .env
