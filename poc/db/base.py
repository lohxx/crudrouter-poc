from sqlalchemy.orm import declarative_base

from poc.db.meta import meta

DeclarativeBase = declarative_base()

class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
