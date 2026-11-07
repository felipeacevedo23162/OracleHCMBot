from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


EMPLOYEE_FIELDS = (
    "WorkFromHome",
    "WorkerCategory",
    "EPS",
    "PensionFund",
    "SeveranceFund",
    "ARL",
    "CCF",
    "RiskLevel",
)


class EmployeeUpdate(BaseModel):
    """Fila normalizada de entrada; los valores vacíos no solicitan cambios."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    person_number: str = Field(alias="PersonNumber", min_length=1)
    WorkFromHome: str | None = None
    WorkerCategory: str | None = None
    EPS: str | None = None
    PensionFund: str | None = None
    SeveranceFund: str | None = None
    ARL: str | None = None
    CCF: str | None = None
    RiskLevel: str | None = None

    @field_validator("person_number", mode="before")
    @classmethod
    def normalize_person_number(cls, value: object) -> str:
        if value is None or value == "":
            raise ValueError("PersonNumber es obligatorio")
        if isinstance(value, bool):
            raise ValueError("PersonNumber no puede ser booleano")
        if isinstance(value, Decimal):
            if value != value.to_integral_value():
                raise ValueError("PersonNumber no puede contener decimales")
            return format(value, "f").split(".")[0]
        if isinstance(value, float):
            if not value.is_integer():
                raise ValueError("PersonNumber no puede contener decimales")
            return str(int(value))
        return str(value).strip()

    def requested_changes(self) -> dict[str, str]:
        return {
            field: value
            for field in EMPLOYEE_FIELDS
            if (value := getattr(self, field)) not in (None, "")
        }
