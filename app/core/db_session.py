from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

SqlAlchemyBase = declarative_base()

__factory = None


def global_init(db_file: str):
    """Initialize async database engine and session factory."""
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a database file.")

    conn_str = f'sqlite+aiosqlite:///{db_file.strip()}'
    print(f"Connecting to DB at {conn_str}")

    engine = create_async_engine(conn_str, echo=False)
    __factory = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    # ⚠️ You cannot call `metadata.create_all()` on an async engine directly
    # You must use a synchronous engine or run migrations with Alembic.
    # So skip create_all or use migrations instead.


def create_session() -> AsyncSession:
    global __factory
    if not __factory:
        raise Exception("DB not initialized. Call global_init() first.")
    return __factory()
