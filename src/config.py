import os

from dotenv import load_dotenv

load_dotenv()


SECRET_TOKEN = os.environ.get("SECRET_TOKEN")

DB_URL = os.environ.get("PSQL_DB_URL")
DB_SYNC_URL = os.environ.get("PSQL_DB_SYNC_URL")

REDIS_URL = os.environ.get("REDIS_URL")
