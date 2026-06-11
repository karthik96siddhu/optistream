from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from app.models.order import OrderStatus

# what the client sends us
class OrderCreate(BaseModel):
    customer_email: EmailStr = Field(..., description='Valid corporate or customer email address')
    product_sku: str = Field(..., min_length=3, max_length=100, description="PROD-XYZ-123") 
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    total_price: float = Field(..., gt=0, description="Total price should be positive decimal value")


# what we return to the client (includes db generated fields)
class OrderResponse(BaseModel):
    id: int
    customer_email: EmailStr
    product_sku: str
    quantity: int
    total_price: float
    status: OrderStatus
    created_at: datetime

    # Tell pydantic to read data even if it's not ORM object (SQLAlchemy model) instead of a dict
    class Config:
        from_attributes = True