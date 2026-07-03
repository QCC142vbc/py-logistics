from src.domain.common.exceptions import DomainException


class OrderNotFoundError(DomainException):
    """Raised when an order cannot be found."""

    pass


class InvalidOrderStatusError(DomainException):
    """Raised when an operation is invalid for the current order status."""

    pass


class OrderProcessingError(DomainException):
    """Raised when order processing fails."""

    pass
