from collections import Counter
from pathlib import Path

import yaml

from models.employee import EMPLOYEE_FIELDS, EmployeeUpdate
from services.excel_service import read_employee_updates


def load_catalogs(path: Path) -> dict[str, set[str]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {field: set(values or []) for field, values in data.items()}


def validate_updates(
    updates: list[EmployeeUpdate], catalogs: dict[str, set[str]]
) -> list[str]:
    errors: list[str] = []
    counts = Counter(update.person_number for update in updates)
    errors.extend(
        f"PersonNumber duplicado: {person_number}"
        for person_number, count in counts.items()
        if count > 1
    )
    for update in updates:
        for field in EMPLOYEE_FIELDS:
            value = getattr(update, field)
            if value not in (None, "") and field in catalogs and value not in catalogs[field]:
                errors.append(
                    f"{update.person_number}: valor no catalogado en {field}: {value}"
                )
    return errors


def validate_file(
    excel_path: Path, catalogs_path: Path
) -> tuple[list[EmployeeUpdate], list[str]]:
    updates = read_employee_updates(excel_path)
    return updates, validate_updates(updates, load_catalogs(catalogs_path))
