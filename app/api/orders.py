from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import OrderService
from app.services.worker_service import WorkerService
from app.services.storage_service import StorageService
from app.schemes.order import OrderCreate, OrderResponse
from app.core.database import get_db, AsyncSessionLocal
from app.models.order import OrderStatus

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

@router.post("/{order_id}/process-invoice", status_code=status.HTTP_202_ACCEPTED)
async def trigger_invoice_processing(
    order_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db) 
):
    """
    Ingest endpoint to trigger invoice generation asynchronously.
    Return HTTP 202 Accepted immediately.
    """
    # Quick structural validation: Does this order even exist
    order = await OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} does not exist. cannot process invoice."
        )

    # Enqueue the slow job to run on the background event queue
    background_tasks.add_task(
        WorkerService.process_invoice_pipeline,
        order_id= order.id,
        db_session_factory = AsyncSessionLocal
    )

    return {
        "message": "Invoice generation pipeline initiated successfully.",
        "order_id": order.id,
        "current_status": order.status
    }


@router.get("/{order_id}/invoice_download_link")
async def get_invoice_download_link(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Generates and returns a secure, temporary cloud URL to download the invoice.
    """
    order = await OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != OrderStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Invoice is not ready. Current order status is: {order.status}"
        )
    
    download_url = StorageService.generate_secure_download_url(order_id=order.id)
    if not download_url:
        raise HTTPException(
            status_code=500,
            detail="Could not generate download path."
        )
    
    return {
        "order_id": order.id,
        "status": order.status,
        "expires_in_seconds": 900,
        "secure_download_url": download_url
    }


        