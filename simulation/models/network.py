from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List

from src.domain.common.models import Location


class NodeType(Enum):
    WAREHOUSE = "warehouse"
    SUPPLIER = "supplier"
    DISTRIBUTION_CENTER = "distribution_center"
    RETAILER = "retailer"


@dataclass
class NetworkNode:
    node_id: str
    node_type: NodeType
    capacity: float
    location: Location
    name: str


@dataclass
class NetworkEdge:
    from_node: str
    to_node: str
    capacity: float
    lead_time: float
    cost: Decimal
    transport_mode: str


@dataclass
class SupplyChainNetwork:
    nodes: List[NetworkNode]
    edges: List[NetworkEdge]

    def get_node(self, node_id: str) -> NetworkNode:
        """Get a node by ID."""
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise ValueError(f"Node {node_id} not found")

    def get_edges_from_node(self, node_id: str) -> List[NetworkEdge]:
        """Get all edges originating from a node."""
        return [edge for edge in self.edges if edge.from_node == node_id]

    def get_edges_to_node(self, node_id: str) -> List[NetworkEdge]:
        """Get all edges terminating at a node."""
        return [edge for edge in self.edges if edge.to_node == node_id]
