from config.settings import settings
from database.database import Database
from PySide6.QtWidgets import QApplication

from gui.main_window import create_window


def main() -> None:
    settings.prepare_directories()
    Database(settings.oracle_database_path).initialize()
    application = QApplication([])
    window = create_window()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()
