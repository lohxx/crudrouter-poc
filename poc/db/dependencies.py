from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from sqlalchemy.orm import Session


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()

def sync_db_session(request: Request):
    session: Session = request.app.state.sync_db_session_factory()

    try:  # noqa: WPS501
        yield session
        session.commit()
    finally:
        session.close()