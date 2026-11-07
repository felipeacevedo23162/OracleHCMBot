from pathlib import Path
from typing import Any

from openpyxl import load_workbook

from models.employee import EmployeeUpdate


REQUIRED_COLUMNS = (
    "PersonNumber",
    "WorkFromHome",
    "WorkerCategory",
    "EPS",
    "PensionFund",
    "SeveranceFund",
    "ARL",
    "CCF",
    "RiskLevel",
)
OPTIONAL_COLUMNS: tuple[str, ...] = ()


def read_employee_updates(path: Path) -> list[EmployeeUpdate]:
    """Lee valores como texto cuando es posible y conserva ceros iniciales."""
    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        worksheet = workbook.active
        rows = worksheet.iter_rows(values_only=True)
        headers = tuple(str(value).strip() if value is not None else "" for value in next(rows))
        missing = [column for column in REQUIRED_COLUMNS if column not in headers]
        if missing:
            raise ValueError(f"Faltan columnas obligatorias: {', '.join(missing)}")
        unknown = set(headers) - set(REQUIRED_COLUMNS) - set(OPTIONAL_COLUMNS)
        if unknown:
            raise ValueError(f"Columnas no soportadas: {', '.join(sorted(unknown))}")
        indexes = {header: index for index, header in enumerate(headers) if header}
        updates: list[EmployeeUpdate] = []
        for row_number, row in enumerate(rows, start=2):
            values: dict[str, Any] = {
                column: row[indexes[column]] if indexes[column] < len(row) else None
                for column in headers
                if column
            }
            if all(value in (None, "") for value in values.values()):
                continue
            updates.append(EmployeeUpdate.model_validate(values))
        return updates
    finally:
        workbook.close()
