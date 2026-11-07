from pathlib import Path

import pytest
from openpyxl import Workbook

from services.excel_service import read_employee_updates


def test_missing_required_column_is_rejected(tmp_path: Path) -> None:
    workbook = Workbook()
    workbook.active.append(["PersonNumber"])
    workbook.active.append(["0007"])
    path = tmp_path / "input.xlsx"
    workbook.save(path)

    with pytest.raises(ValueError, match="Faltan columnas"):
        read_employee_updates(path)
