from dataclasses import dataclass

from src.application.dto.common import AddressDTO
from src.application.dto.supplier import SupplierDTO
from src.domain.supplier.models import Address, Supplier
from src.domain.supplier.services import SupplierService


@dataclass
class RegisterSupplierRequest:
    name: str
    contact_email: str
    phone: str
    address: AddressDTO
    payment_terms: str
    lead_time_days: int
    contact_person: str = None
    website: str = None
    tax_id: str = None
    notes: str = None
    categories: list = None


@dataclass
class RegisterSupplierResponse:
    supplier_id: str
    status: str


class RegisterSupplierUseCase:
    def __init__(self, supplier_service: SupplierService) -> None:
        self._supplier_service = supplier_service

    async def execute(self, request: RegisterSupplierRequest) -> RegisterSupplierResponse:
        address = Address(
            street=request.address.street,
            city=request.address.city,
            state=request.address.state,
            postal_code=request.address.postal_code,
            country=request.address.country,
            address_line2=request.address.address_line2,
        )

        supplier = Supplier(
            id=None,
            name=request.name,
            contact_email=request.contact_email,
            phone=request.phone,
            address=address,
            rating=3.0,  # Default rating for new suppliers
            active=True,
            payment_terms=request.payment_terms,
            lead_time_days=request.lead_time_days,
            contact_person=request.contact_person,
            website=request.website,
            tax_id=request.tax_id,
            notes=request.notes,
            categories=request.categories or [],
        )

        created_supplier = await self._supplier_service.register_supplier(supplier)

        return RegisterSupplierResponse(
            supplier_id=created_supplier.id,
            status="registered",
        )
