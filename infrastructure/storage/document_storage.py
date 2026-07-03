from src.infrastructure.storage.s3_client import S3Client


class DocumentStorage:
    def __init__(self, s3_client: S3Client) -> None:
        self._s3 = s3_client

    async def save_invoice(
        self,
        order_id: str,
        invoice_pdf: bytes,
    ) -> str:
        """Save an invoice PDF to storage."""
        key = f"invoices/{order_id}.pdf"
        return await self._s3.upload_file(
            key=key,
            invoice_pdf,
            content_type="application/pdf",
        )

    async def get_invoice(self, order_id: str) -> bytes:
        """Retrieve an invoice PDF from storage."""
        key = f"invoices/{order_id}.pdf"
        return await self._s3.download_file(key)
