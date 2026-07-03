from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AuditAction:
    action_type: str
    entity_type: str
    entity_id: str
    performed_by: str
    timestamp: datetime
    details: dict = None


@dataclass
class AuditEntry:
    id: str
    action: AuditAction
    timestamp: datetime


@dataclass
class AuditFilter:
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    performed_by: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class AuditRepository:
    async def log_action(self, action: AuditAction) -> None:
        """Log an audit action."""
        pass

    async def get_audit_log(self, filter: AuditFilter) -> List[AuditEntry]:
        """Retrieve audit log based on filter."""
        pass


class AuditService:
    def __init__(self, audit_repository: AuditRepository) -> None:
        self._audit_repository = audit_repository

    async def log_action(self, action: AuditAction) -> None:
        """Log an action to the audit trail."""
        await self._audit_repository.log_action(action)

    async def get_audit_log(self, filter: AuditFilter) -> List[AuditEntry]:
        """Retrieve audit log entries."""
        return await self._audit_repository.get_audit_log(filter)
