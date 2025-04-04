from litestar import Router, get
from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import OKSRecord
from dependencies import provide_session

@get("/oks")
async def list_oks(db_session: AsyncSession = Provide(provide_session)) -> list[dict]:
    result = await db_session.execute(select(OKSRecord))
    rows = result.scalars().all()
    return [{k: v for k, v in row.__dict__.items() if not k.startswith("_")} for row in rows]

@get("/oks/uin/{uin:str}")
async def get_by_uin(uin: str, db_session: AsyncSession = Provide(provide_session)) -> dict:
    result = await db_session.execute(select(OKSRecord).where(OKSRecord.uin == uin))
    row = result.scalar_one_or_none()
    return {k: v for k, v in row.__dict__.items() if not k.startswith("_")} if row else {}

@get("/OKSRecord/klass/{klass:str}")
async def get_by_klass(klass: str, db_session: AsyncSession = Provide(provide_session)) -> list[dict]:
    result = await db_session.execute(select(OKSRecord).where(OKSRecord.klass == klass))
    rows = result.scalars().all()
    return [{k: v for k, v in row.__dict__.items() if not k.startswith("_")} for row in rows]

@get("/OKSRecord/subclass3/{subclass3:str}")
async def get_by_subclass_3(subclass3: str, db_session: AsyncSession = Provide(provide_session)) -> dict:
    result = await db_session.execute(select(OKSRecord).where(OKSRecord.subclass_3 == subclass3))
    row = result.scalar_one_or_none()
    return {k: v for k, v in row.__dict__.items() if not k.startswith("_")} if row else {}

oks_router = Router(path="", tags=["OKS"], route_handlers=[
    list_oks,
    get_by_uin,
    get_by_klass,
    get_by_subclass_3,
])
