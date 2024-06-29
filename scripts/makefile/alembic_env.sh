# Update alembic/env.py
ENV_PY="alembic/env.py"

# Insert imports at the 9th and 10th lines
sed -i'' '9i\
from core.settings import settings
' $ENV_PY

sed -i'' '10i\
from core.models import Base
' $ENV_PY

# Update target.metadata to Base.metadata
sed -i'' "s|target_metadata = None|target_metadata = Base.metadata|" $ENV_PY

# Set the sqlalchemy.url option in the config
sed -i'' "31i\
config.set_main_option('sqlalchemy.url', str(settings.db.postgres.url))
" $ENV_PY

echo "Updated alembic/env.py with necessary imports and configurations."