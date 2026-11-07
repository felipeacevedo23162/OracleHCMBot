from pathlib import Path

from database.database import Database


def test_database_initializes_and_detects_uncertain_submission(tmp_path: Path) -> None:
    database = Database(tmp_path / "state.sqlite3")
    database.initialize()

    assert database.has_uncertain_submission("0001") is False
