from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TransactionStatus(StrEnum):
    PENDIENTE = "PENDIENTE"
    VALIDADO = "VALIDADO"
    EN_PROCESO = "EN_PROCESO"
    REVISADO = "REVISADO"
    APROBADO = "APROBADO"
    ENVIADO = "ENVIADO"
    EXITOSO = "EXITOSO"
    ERROR = "ERROR"
    PENDIENTE_VERIFICACION = "PENDIENTE_VERIFICACION"
    CANCELADO = "CANCELADO"


class FieldChange(BaseModel):
    field: str
    previous_value: str | None = None
    requested_value: str


class TransactionRecord(BaseModel):
    execution_id: str
    person_number: str
    status: TransactionStatus = TransactionStatus.PENDIENTE
    changes: list[FieldChange] = Field(default_factory=list)
    oracle_message: str | None = None
    transaction_id: str | None = None
    verification_result: str | None = None
    duration_ms: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
