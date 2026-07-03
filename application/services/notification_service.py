from typing import List


class EmailClient:
    async def send_email(self, to: str, subject: str, body: str) -> None:
        """Send an email."""
        pass


class SMSClient:
    async def send_sms(self, to: str, message: str) -> None:
        """Send an SMS message."""
        pass


class NotificationService:
    def __init__(self, email_client: EmailClient, sms_client: SMSClient) -> None:
        self._email_client = email_client
        self._sms_client = sms_client

    async def send_order_confirmation(self, order_id: str, customer_email: str) -> None:
        """Send order confirmation email."""
        subject = f"Order Confirmation - {order_id}"
        body = f"Your order {order_id} has been confirmed."
        await self._email_client.send_email(customer_email, subject, body)

    async def send_shipment_update(self, shipment_id: str, recipient: str) -> None:
        """Send shipment update notification."""
        subject = f"Shipment Update - {shipment_id}"
        body = f"Your shipment {shipment_id} status has been updated."
        await self._email_client.send_email(recipient, subject, body)

    async def send_low_stock_alert(self, item_id: str, recipients: List[str]) -> None:
        """Send low stock alert to recipients."""
        subject = f"Low Stock Alert - Item {item_id}"
        body = f"Item {item_id} is below reorder point."
        for recipient in recipients:
            await self._email_client.send_email(recipient, subject, body)
