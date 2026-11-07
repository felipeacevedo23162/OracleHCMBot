from pathlib import Path

import pytest

from core.exceptions import ConfigurationError
from core.oracle_bot import load_verified_selectors


def test_unconfigured_selectors_block_execution(tmp_path: Path) -> None:
    selectors = tmp_path / "selectors.yaml"
    selectors.write_text("form:\n  field: NO_CONFIGURADO\n", encoding="utf-8")

    with pytest.raises(ConfigurationError):
        load_verified_selectors(selectors)
