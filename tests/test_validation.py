from pathlib import Path

from openpyxl import Workbook

from services.validation_service import validate_file


def make_workbook(path: Path, rows: list[list[object]]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(
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
    for row in rows:
        sheet.append([row[0], None, None, None, None, None, None, None, row[1]])
    workbook.save(path)


def test_duplicate_person_numbers_are_rejected(tmp_path: Path) -> None:
    excel = tmp_path / "input.xlsx"
    catalogs = tmp_path / "catalogs.yaml"
    make_workbook(excel, [["0007", "I"], ["0007", "I"]])
    catalogs.write_text("RiskLevel: [I]\n", encoding="utf-8")

    updates, errors = validate_file(excel, catalogs)

    assert len(updates) == 2
    assert any("duplicado" in error for error in errors)


def test_catalog_values_are_rejected(tmp_path: Path) -> None:
    excel = tmp_path / "input.xlsx"
    catalogs = tmp_path / "catalogs.yaml"
    make_workbook(excel, [["0007", "NO_EXISTE"]])
    catalogs.write_text("RiskLevel: [I]\n", encoding="utf-8")

    _, errors = validate_file(excel, catalogs)

    assert any("no catalogado" in error for error in errors)
