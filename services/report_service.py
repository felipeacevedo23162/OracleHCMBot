from pathlib import Path

from openpyxl import Workbook

from database.database import Database


def export_transactions(database: Database, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(
        ["execution_id", "person_number", "status", "oracle_message",
         "transaction_id", "verification_result", "updated_at"]
    )
    import sqlite3
    with sqlite3.connect(database.path) as connection:
        rows = connection.execute(
            "SELECT execution_id, person_number, status, oracle_message, "
            "transaction_id, verification_result, updated_at FROM transactions"
        )
        for row in rows:
            sheet.append(list(row))
    workbook.save(output)
