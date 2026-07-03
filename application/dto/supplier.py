from dataclasses import dataclass


@dataclass
class SupplierDTO:
    id: str
    name: str
    contact_email: str
    rating: float
    active: bool


@dataclass
class SupplierScoreDTO:
    supplier_id: str
    reliability_score: float
    quality_score: float
    cost_score: float
    overall_score: float
