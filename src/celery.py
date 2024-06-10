from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import REDIS_URL, DB_SYNC_URL

# Initialize Celery
celery = Celery(
    'tasks',
    broker=REDIS_URL + '/0',
    backend=REDIS_URL + '/1',
)


# Create SQLAlchemy engine
engine = create_engine(DB_SYNC_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Include tasks
celery.autodiscover_tasks()
