import json

from sqlalchemy import text, select
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from poc.db.filters import EqFilter, GteFilter, LtFilter, NeFilter, InFilter
from poc.db.filters import FilterNotSupported, OPERATORS

from poc.settings import settings
from poc.db.models import todos

async def create_database() -> None:
    """Create a database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")

    async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{settings.db_base}'",  # noqa: E501, S608
            ),
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f'CREATE DATABASE "{settings.db_base}" ENCODING "utf8" TEMPLATE template1',  # noqa: E501
            ),
        )


async def drop_database() -> None:
    """Drop current database."""
    db_url = make_url(str(settings.db_url.with_path("/postgres")))
    engine = create_async_engine(db_url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        disc_users = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "  # noqa: S608
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{settings.db_base}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(text(disc_users))
        await conn.execute(text(f'DROP DATABASE "{settings.db_base}"'))



def get_all_tasks(db_session, model, page=1, per_page=20, extra_filters=None):
    query = db_session.query(model)
    if extra_filters:
        extra_filters = json.loads(extra_filters)
        for k, v in extra_filters.items():
            if isinstance(v, dict):
                for op, value in v.items():
                    if op not in OPERATORS:
                        raise FilterNotSupported(f"Operator {op} is not supported")
                    operator = OPERATORS[op]()
                    query = query.filter(text(f"{k} {str(operator)} {operator.converter(value)}"))
            else:
                operator = OPERATORS['$eq']()
                query = query.filter(text(f"{k} {str(operator)} {operator.converter(value)}"))

    query = query.limit(per_page).offset((page - 1) * per_page)
    return db_session.execute(query).all()
