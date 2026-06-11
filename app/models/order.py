import enum
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Index
from datetime import datetime
from app.core.database import Base

class OrderStatus(enum.Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    FAILED = 'failed'

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_email = Column(String(255), nullable=False)
    product_sku = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # composite index for faster analytical queries.
    __table_args__ = (
        Index('idx_customer_status', 'customer_email', 'status'),
    )
