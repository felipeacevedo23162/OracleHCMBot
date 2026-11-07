from pathlib import Path
from typing import Any

import yaml

from core.exceptions import ConfigurationError


def load_verified_selectors(path: Path) -> dict[str, Any]:
    """Carga selectores y rechaza cualquier marcador no verificado."""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    def walk(value: Any, location: str = "root") -> None:
        if value == "NO_CONFIGURADO":
            raise ConfigurationError(
                f"Selector no configurado; operación bloqueada: {location}"
            )
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, f"{location}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{location}[{index}]")

    walk(data)
    return data


class OracleBot:
    """Fachada segura; no permite operaciones productivas sin configuración."""

    def __init__(self, selectors_path: Path) -> None:
        self.selectors_path = selectors_path

    def ensure_ready(self) -> None:
        load_verified_selectors(self.selectors_path)

    def start_manual_session(self) -> None:
        self.ensure_ready()
        raise NotImplementedError(
            "La sesión Playwright se habilitará después de verificar selectores "
            "y el DOM accesible del entorno autorizado."
        )
