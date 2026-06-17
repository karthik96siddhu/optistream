from botocore.exceptions import ClientError
from app.core.s3_client import get_s3_client, S3_BUCKET_NAME

class StorageService:

    @staticmethod
    def generate_secure_download_url(order_id: int, expires_in_second: int = 900) -> str | None:
        """
        Generate a secure time-bound  presigned download URL for a specific order invoice
        Default to 900 seconds (15 minutes)
        """
        s3_client = get_s3_client()
        s3_key = f"invoices/invoice_order_{order_id}.pdf"
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params = {
                    'Bucket': S3_BUCKET_NAME,
                    "Key": s3_key
                },
                ExpiresIn = expires_in_second
            )
            return url
        except ClientError as e:
            print(f"[STORAGE SERVICE] error generating presigned URL: {e}")
            return None
        
