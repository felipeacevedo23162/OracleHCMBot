import sqlite3
from pathlib import Path


class Database:
    """Persistencia local de estado y auditoría, sin credenciales ni cookies."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS transactions (
                    execution_id TEXT NOT NULL,
                    person_number TEXT NOT NULL,
                    status TEXT NOT NULL,
                    oracle_message TEXT,
                    transaction_id TEXT,
                    verification_result TEXT,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (execution_id, person_number)
                );
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    execution_id TEXT NOT NULL,
                    person_number TEXT NOT NULL,
                    field_name TEXT,
                    previous_value TEXT,
                    requested_value TEXT,
                    status TEXT NOT NULL,
                    oracle_message TEXT,
                    transaction_id TEXT,
                    duration_ms INTEGER,
                    created_at TEXT NOT NULL
                );
                """
            )

    def has_uncertain_submission(self, person_number: str) -> bool:
        with sqlite3.connect(self.path) as connection:
            row = connection.execute(
                """SELECT 1 FROM transactions
                   WHERE person_number = ?
                     AND status = 'PENDIENTE_VERIFICACION'
                   LIMIT 1""",
                (person_number,),
            ).fetchone()
        return row is not None
