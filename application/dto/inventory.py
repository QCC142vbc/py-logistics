from dataclasses import dataclass


@dataclass
class ItemDTO:
    id: str
    sku: str
    name: str
    quantity: int
    unit_cost: str
    location: str
    category: str


@dataclass
class StockLevelDTO:
    item_id: str
    available: int
    reserved: int
    in_transit: int
