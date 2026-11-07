import os
from pathlib import Path

import pytest
from openpyxl import Workbook
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


@pytest.fixture(scope="session")
def qapp() -> QApplication:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    return QApplication.instance() or QApplication([])


def test_window_loads_excel_and_reports_catalog_errors(
    qapp: QApplication, tmp_path: Path
) -> None:
    workbook = Workbook()
    workbook.active.append(
        [
            "PersonNumber",
            "WorkFromHome",
            "WorkerCategory",
            "EPS",
            "PensionFund",
            "SeveranceFund",
            "ARL",
            "CCF",
            "RiskLevel",
        ]
    )
    workbook.active.append(["0007", None, None, None, None, None, None, None, None])
    path = tmp_path / "input.xlsx"
    workbook.save(path)

    window = MainWindow()
    window.load_excel(path)

    assert window.table.rowCount() == 1
    assert window.table.item(0, 0).text() == "0007"
