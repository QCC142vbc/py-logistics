from dataclasses import dataclass


@dataclass
class GetUtilizationRequest:
    warehouse_id: str


@dataclass
class GetUtilizationResponse:
    warehouse_id: str
    utilization_percentage: float
    available_capacity_sqm: float


class GetUtilizationUseCase:
    def __init__(self, warehouse_service) -> None:
        self._warehouse_service = warehouse_service

    async def execute(self, request: GetUtilizationRequest) -> GetUtilizationResponse:
        utilization = await self._warehouse_service.get_warehouse_utilization(request.warehouse_id)
        warehouse = await self._warehouse_service.get_warehouse(request.warehouse_id)

        return GetUtilizationResponse(
            warehouse_id=request.warehouse_id,
            utilization_percentage=utilization,
            available_capacity_sqm=warehouse.available_capacity_sqm,
        )
