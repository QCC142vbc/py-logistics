class DomainException(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(self, message: str, details: dict = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        return self.message


class ValidationException(DomainException):
    """Raised when validation fails."""

    pass


class NotFoundException(DomainException):
    """Raised when a requested entity is not found."""

    pass


class BusinessRuleException(DomainException):
    """Raised when a business rule is violated."""

    pass
