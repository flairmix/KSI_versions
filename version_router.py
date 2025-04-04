from litestar import Router, get, post, Request
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import DatasetVersion, OKSRecord
from dependencies import provide_session
import pandas as pd
import uuid

@get("/versions")
async def list_versions(db_session: AsyncSession = Provide(provide_session)) -> list[dict]:
    result = await db_session.execute(select(DatasetVersion).order_by(DatasetVersion.uploaded_at.desc()))
    rows = result.scalars().all()
    return [
        {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
        for row in rows
    ]

@get("/versions/{version_id:int}")
async def get_version(version_id: int, db_session: AsyncSession = Provide(provide_session)) -> dict:
    result = await db_session.execute(select(DatasetVersion).where(DatasetVersion.id == version_id))
    row = result.scalar_one_or_none()
    return {k: v for k, v in row.__dict__.items() if not k.startswith("_")} if row else {}

@get("/versions/{version_id:int}/records")
async def get_records_for_version(version_id: int, db_session: AsyncSession = Provide(provide_session)) -> list[dict]:
    result = await db_session.execute(select(OKSRecord).where(OKSRecord.version_id == version_id))
    rows = result.scalars().all()
    return [
        {k: v for k, v in row.__dict__.items() if not k.startswith("_")}
        for row in rows
    ]


version_router = Router(path="versions", tags=["versions"], route_handlers=[
    list_versions,
    get_version,
    get_records_for_version,
])
