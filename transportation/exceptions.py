from src.domain.common.exceptions import DomainException


class ShipmentNotFoundError(DomainException):
    """Raised when a shipment cannot be found."""

    pass


class RouteNotFoundError(DomainException):
    """Raised when a route cannot be found."""

    pass


class CarrierUnavailableError(DomainException):
    """Raised when a carrier is unavailable for a request."""

    pass
