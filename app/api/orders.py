from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import OrderService
from app.schemes.order import OrderCreate, OrderResponse
from app.core.database import get_db

router = APIRouter(prefix='/orders', tags=['orders'])

@router.post('/', response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        order = await OrderService.create_new_order(db=db, order_data=payload)
        return order
    except Exception as e:
        # Log error in production with proper logging framework instead of print
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist transaction. Please try again later."
        )

@router.get('/{order_id}', response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await OrderService.get_order_by_id(db=db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Order with ID {order_id} not found."
        )
    return order
        