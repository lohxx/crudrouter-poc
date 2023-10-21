from sqlalchemy.orm import DeclarativeBase

from poc.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
