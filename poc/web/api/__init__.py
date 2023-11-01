"""poc API package."""
from enum import Enum
from copy import deepcopy
from typing import Optional, List

from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from pydantic import BaseModel, validator

from sqlalchemy.orm import Query

from poc.db.dependencies import sync_db_session
from poc.db.utils import get_all_entities, update_entity as update_entity_db


class OrmBase(BaseModel):
    # Common properties across orm models
    id: int

    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True



def create_router(schema: BaseModel, create_schema: BaseModel, model, prefix: str, partial_model=None, db=sync_db_session):
    """
    Create a CRUD router for a given model.

    Args:
        schema (BaseModel): Pydantic schema for the model.
        create_schema (BaseModel): Pydantic schema for post requests.
        model (_type_): SQLAlchemy model.
        prefix (str): Api path prefix.
        partial_model (BaseModel): Pydantic model used for patch/put requests. Defaults to None.
        db (_type_, optional): SQLAlchemy session. Defaults to sync_db_session.

    Returns:
        SQLAlchemyCRUDRouter: api router.
    """    
    partial_model = create_schema if partial_model is None else partial_model

    router = SQLAlchemyCRUDRouter(
        schema=schema,
        create_schema=create_schema,
        update_schema=partial_model,
        db_model=model,
        db=db,
        prefix=prefix,
        delete_all_route=False
    )

    @router.api_route('/{item_id}', methods=['PATCH'])
    def update_task(
        item_id: int,
        body: partial_model,
        db_session=Depends(sync_db_session)) -> schema:
        task = update_entity_db(db_session, item_id, body, model)
        return schema.from_orm(task)


    @router.get('')
    def get_all(
        where: Optional[str] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 20,
        db_session=Depends(sync_db_session),
    ) -> Optional[List[schema]]:
        entities = get_all_entities(db_session, model, page, per_page, extra_filters=where)
        return [schema.from_orm(entity) for entity in entities]

    return router