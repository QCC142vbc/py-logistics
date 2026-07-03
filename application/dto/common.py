from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressDTO:
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    address_line2: Optional[str] = None
