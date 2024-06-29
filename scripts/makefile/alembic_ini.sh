#!/bin/sh
# The script is called from Makefile
SRC_DIR=$(grep "SRC_DIR" config.toml | sed 's/.*= *//;s/"//g')

if [ -z "$SRC_DIR" ]; then
  echo "SRC_DIR is not found in config.toml"
  exit 1
fi

# Update the value of prepend_sys_path in alembic.ini
sed -i'' "s|prepend_sys_path = .*|prepend_sys_path = ./$SRC_DIR|" alembic.ini

# Uncomment the file_template line
sed -i'' "s|# file_template =|file_template =|" alembic.ini

# Uncomment the black hook lines
sed -i'' "s|# hooks = black|hooks = black|" alembic.ini
sed -i'' "s|# black.type =|black.type =|" alembic.ini
sed -i'' "s|# black.entrypoint =|black.entrypoint =|" alembic.ini
sed -i'' "s|# black.options =|black.options =|" alembic.ini

echo "Updated alembic.ini with SRC_DIR and uncommented specified lines."
