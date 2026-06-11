from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.order import Order
from app.schemes.order import OrderCreate

class OrderService:

    @staticmethod
    async def create_new_order(db: AsyncSession, order_data: OrderCreate) -> Order:
        # Transform pydantic validation schema into an actual SQLAlchemy ORM entity

        new_order = Order(
            customer_email=order_data.customer_email,
            product_sku=order_data.product_sku,
            quantity=order_data.quantity,
            total_price=order_data.total_price
        )

        db.add(new_order)
        await db.commit() # Trigger asynchronous I/O write operation
        await db.refresh(new_order) # Reload state from DB to obtain auto-incremented ID
        return new_order

    @staticmethod
    async def get_order_by_id(db: AsyncSession, order_id: int) -> Order:
        # construct an explicit, asynchronous modern SQLAlchemy 2.0 select query
        query = select(Order).where(Order.id == order_id)
        result = await db.execute(query) 
        return result.scalars().first() # Extract the first Order object from the result set, or None if not found
    
