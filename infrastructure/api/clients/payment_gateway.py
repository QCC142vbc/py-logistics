from dataclasses import dataclass
from decimal import Decimal

import httpx


@dataclass
class PaymentRequest:
    amount: Decimal
    currency: str
    card_token: str
    customer_id: str
    order_id: str


@dataclass
class PaymentResponse:
    success: bool
    transaction_id: str
    amount: Decimal
    status: str


@dataclass
class RefundResponse:
    success: bool
    refund_id: str
    amount: Decimal
    status: str


class PaymentGatewayAPIClient:
    def __init__(self, api_key: str, secret: str) -> None:
        self._api_key = api_key
        self._secret = secret
        self._base_url = "https://api.payment-gateway.com"
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Secret": secret,
            }
        )

    async def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        """Process a payment."""
        response = await self._client.post(
            f"{self._base_url}/payments",
            json={
                "amount": str(request.amount),
                "currency": request.currency,
                "card_token": request.card_token,
                "customer_id": request.customer_id,
                "order_id": request.order_id,
            },
        )
        response.raise_for_status()
        data = response.json()
        
        return PaymentResponse(
            success=data["success"],
            transaction_id=data["transaction_id"],
            amount=Decimal(str(data["amount"])),
            status=data["status"],
        )

    async def refund_payment(
        self,
        transaction_id: str,
        amount: Decimal,
    ) -> RefundResponse:
        """Refund a payment."""
        response = await self._client.post(
            f"{self._base_url}/refunds",
            json={
                "transaction_id": transaction_id,
                "amount": str(amount),
            },
        )
        response.raise_for_status()
        data = response.json()
        
        return RefundResponse(
            success=data["success"],
            refund_id=data["refund_id"],
            amount=Decimal(str(data["amount"])),
            status=data["status"],
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
