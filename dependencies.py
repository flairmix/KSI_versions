from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Поддержка версионности через отдельную БД или таблицы версий
DATABASE_URL = "sqlite+aiosqlite:///oks.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # пригодится при многосессионной работе
)

AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

def provide_session() -> AsyncSession:
    return AsyncSessionLocal()
