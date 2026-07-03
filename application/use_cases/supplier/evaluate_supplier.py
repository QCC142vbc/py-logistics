from dataclasses import dataclass

from src.application.dto.supplier import SupplierScoreDTO
from src.domain.supplier.models import SupplierScore
from src.domain.supplier.services import SupplierService


@dataclass
class EvaluateSupplierRequest:
    supplier_id: str


@dataclass
class EvaluateSupplierResponse:
    supplier_id: str
    scores: SupplierScoreDTO


class EvaluateSupplierUseCase:
    def __init__(self, supplier_service: SupplierService) -> None:
        self._supplier_service = supplier_service

    async def execute(self, request: EvaluateSupplierRequest) -> EvaluateSupplierResponse:
        score = await self._supplier_service.evaluate_supplier(request.supplier_id)

        score_dto = SupplierScoreDTO(
            supplier_id=score.supplier_id,
            reliability_score=score.reliability_score,
            quality_score=score.quality_score,
            cost_score=score.cost_score,
            overall_score=score.overall_score,
        )

        return EvaluateSupplierResponse(
            supplier_id=request.supplier_id,
            scores=score_dto,
        )
