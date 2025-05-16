from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

SqlAlchemyBase = declarative_base()

__factory = None


async def global_init(db_file: str):
    """Initialize async database engine and session factory."""
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a database file.")

    conn_str = f'sqlite+aiosqlite:///{db_file.strip()}'
    print(f"Connecting to DB at {conn_str}")

    engine = create_async_engine(conn_str, echo=True)
    __factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    # Proper async table creation
    async with engine.begin() as conn:
        await conn.run_sync(SqlAlchemyBase.metadata.create_all)


def create_session() -> AsyncSession:
    if not __factory:
        raise Exception("DB not initialized. Call await global_init() first.")
    return __factory()