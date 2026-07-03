from src.domain.common.exceptions import DomainException


class SupplierNotFoundError(DomainException):
    """Raised when a supplier cannot be found."""

    pass


class DuplicateSupplierError(DomainException):
    """Raised when attempting to create a duplicate supplier."""

    pass
