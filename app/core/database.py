import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", 'mysql+aiomysql://user:password@localhost:3306/optistream')

# create async engine
# pool size and max overflow are critical for production tuning to manage concurrent connections.
async_engine = create_async_engine(
    DATABASE_URL,
    echo= True, # Set to False in production; True helps us debug SQL queries.
    pool_size=20, # Keeps 20 persistent connections open.
    max_overflow=10 # Allows upto 10 additional connections if pool is exausted.
)

# create an asynchronous session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_ = AsyncSession,
    expire_on_commit = False, # Prvents SQLAlchemy from doing lazy loads on expired attributes
)

Base = declarative_base() # Base class for our ORM models

# Dependency Injection function to yield database sessions to endpoints 
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() # Ensure session is closed after use to free up connections
