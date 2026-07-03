from src.domain.common.exceptions import DomainException


class WarehouseNotFoundError(DomainException):
    """Raised when a warehouse cannot be found."""

    pass


class InsufficientCapacityError(DomainException):
    """Raised when there is insufficient capacity for an operation."""

    pass


class StorageLocationNotFoundError(DomainException):
    """Raised when a storage location cannot be found."""

    pass
