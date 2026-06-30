import pytest, os
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.main import app
from app.core.database import get_db, Base

# Dedicated, isolated Test Database URL (use a separate test DB name)
TEST_DB_URL = os.getenv("TEST_DATABASE_URL", "mysql+aiomysql://user:password@localhost:3306/optistream_test")

test_engine = create_async_engine(TEST_DB_URL, echo=False)
TestingSessionLocal = async_sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="function", autouse=True)
async def setup_test_db():
    """
    Before each test runs, create all tables
    After the test finishes, drop all the tables to keep a pristine slate
    """

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session():
    """Provide an isolated database transaction per test function"""
    async with TestingSessionLocal as session:
        yield session
    
@pytest.fixture
async def async_client(db_session):
    """
    Overrides the operational get_db dependency in FastAPI
    with our prestine, isolated testing database session.
    """

    async def _override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_db] = _override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
