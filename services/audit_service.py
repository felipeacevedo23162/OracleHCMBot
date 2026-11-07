from datetime import datetime, timezone
import sqlite3

from models.transaction import TransactionRecord
from database.database import Database


def record_transaction(database: Database, record: TransactionRecord) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    with sqlite3.connect(database.path) as connection:
        connection.execute(
            """INSERT OR REPLACE INTO transactions
               (execution_id, person_number, status, oracle_message,
                transaction_id, verification_result, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                record.execution_id,
                record.person_number,
                record.status.value,
                record.oracle_message,
                record.transaction_id,
                record.verification_result,
                timestamp,
            ),
        )
        for change in record.changes:
            connection.execute(
                """INSERT INTO audit_events
                   (execution_id, person_number, field_name, previous_value,
                    requested_value, status, oracle_message, transaction_id,
                    duration_ms, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    record.execution_id,
                    record.person_number,
                    change.field,
                    change.previous_value,
                    change.requested_value,
                    record.status.value,
                    record.oracle_message,
                    record.transaction_id,
                    record.duration_ms,
                    timestamp,
                ),
            )
