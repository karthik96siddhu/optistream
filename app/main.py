from fastapi import FastAPI
from app.core.database import async_engine, Base
from app.api.orders import router as order_router_v1

app = FastAPI(
    title="Optistream API",
    description="High-throughput Event-Driven Asynchronous Backend Architecture",
    version="1.0.0"
)

@app.on_event("startup")
async def on_startup():
    # In development, we can create tables directly
    # (In Phase 2, we will migrate to use alembic)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine": "asynchronous api test"}

# Include API routers
app.include_router(order_router_v1, prefix="/api/v1")


