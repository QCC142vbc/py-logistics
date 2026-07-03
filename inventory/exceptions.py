from src.domain.common.exceptions import DomainException


class ItemNotFoundError(DomainException):
    """Raised when an item cannot be found."""

    pass


class InsufficientStockError(DomainException):
    """Raised when there is insufficient stock for an operation."""

    pass


class InvalidSKUError(DomainException):
    """Raised when an SKU is invalid."""

    pass
