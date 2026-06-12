import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import OrderService
from app.services.invoice_service import InvoiceService
from app.models.order import OrderStatus

class WorkerService:

    @staticmethod
    async def process_invoice_pipeline(order_id: int, db_session_factory) -> None:
        """"
        Background worker pipeline.
        Accepts a session factory instead of an active session, as background tasks
        often outlive the lifetime of the request scope session.
        """
        print(f"[BACKGROUND WORKER] Initializing invoice processing for order ID: {order_id}")

        # Open complete fresh, decoupled database connection for the background run
        async with db_session_factory() as db:
            order = await OrderService.get_order_by_id(db=db, order_id=order_id)
            if not order:
                print(f"[BACKGROUND WORKER] Error: Order {order_id} not found")
                return
            
            try:
                # Update status to indicate processing has started
                order.status = OrderStatus.PROCESSING
                await db.commit()

                # Run the heavy CPU-bound PDF generation inside an external thread pool
                # to prevent blocking asynchronous event loop.
                loop = asyncio.get_running_loop()
                local_pdf_path = await loop.run_in_executor(
                    None,
                    InvoiceService.generate_pdf_invoice,
                    order
                )

                # NOTE: Phase 5 we will inject AWS s3 upload here using local_pdf_path

                # Mark as complete upon successfull processing
                order.status = OrderStatus.COMPLETED
                await db.commit()
                print(f"[BACKGROUND WORKER] Order {order_id} pipeline completed successfully.")
            except Exception as e:
                # Robust error handling ensure a crash doesn't hang the worker indefinitely.
                await db.rollback()
                order.status = OrderStatus.FAILED
                await db.commit()
                print(f"[BACKGROUND WORKER] Pipeline failed for Order {order_id}. Error: str{e}")