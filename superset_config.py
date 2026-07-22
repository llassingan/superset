import os

from sqlalchemy.engine.url import URL

SECRET_KEY = os.getenv(
    "SUPERSET_SECRET_KEY",
    "rdajuara1"
)

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://"
    f"{os.environ['DATABASE_USER']}:"
    f"{os.environ['DATABASE_PASSWORD']}@"
    f"{os.environ['DATABASE_HOST']}:"
    f"{os.environ['DATABASE_PORT']}/"
    f"{os.environ['DATABASE_DB']}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

ROW_LIMIT = 100000

FEATURE_FLAGS = {
    "ALERT_REPORTS": False,
    "ENABLE_SUPERSET_META_DB": True,
}

SUPERSET_META_DB_LIMIT = 50000
ENABLE_PROXY_FIX = True
