import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.order_service import OrderService
from app.services.invoice_service import InvoiceService
from app.models.order import OrderStatus
from app.core.s3_client import get_s3_client, S3_BUCKET_NAME

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

                # Upload the file to S3/MinIO using standard boto3 calls
                s3_key = f"invoices/invoice_order_{order_id}.pdf"
                s3_client = get_s3_client()

                print(f"[BACKGROUND WORKER] Uploading {s3_key} to bucket: {S3_BUCKET_NAME}...")

                #run in executor since boto3 upload_file is a synchronous, blocking network I/O call.
                await loop.run_in_executor(
                    None,
                    s3_client.upload_file,
                    local_pdf_path, # local source path
                    S3_BUCKET_NAME, # destination path
                    s3_key          # storage path key inside bucket
                )

                # Cleanup: Remove local file rom server disk to optimise system storage.
                if os.path.exists(local_pdf_path):
                    os.remove(local_pdf_path)
                    print(f"[BACKGROUND WORKER] Temporary local file removed")
                

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