from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    """Configuración centralizada y segura de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    oracle_base_url: str = Field(default="")
    oracle_browser_channel: str = Field(default="msedge")
    oracle_headless: bool = Field(default=False)
    oracle_timeout_ms: int = Field(default=15_000, ge=1_000)
    oracle_profile_dir: Path = Field(default=ROOT_DIR / ".browser-profile")
    oracle_allowed_transaction: str = Field(default="Actualizar")
    oracle_simulation_required: bool = Field(default=True)
    oracle_database_path: Path = Field(
        default=ROOT_DIR / "data" / "oracle_hcm_bot.sqlite3"
    )
    oracle_reports_dir: Path = Field(default=ROOT_DIR / "reports")
    oracle_logs_dir: Path = Field(default=ROOT_DIR / "logs")

    def prepare_directories(self) -> None:
        for directory in (
            self.oracle_profile_dir,
            self.oracle_database_path.parent,
            self.oracle_reports_dir,
            self.oracle_logs_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


settings = Settings()
