from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from config.settings import ROOT_DIR, settings
from services.validation_service import validate_file


class MainWindow(QMainWindow):
    """Ventana principal para validar entradas sin iniciar transacciones Oracle."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OracleHCMBot")
        self.resize(900, 600)
        self._build_ui()

    def _build_ui(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)

        self.status_label = QLabel(
            "Estado Oracle: bloqueado hasta verificar sesión y selectores"
        )
        self.file_label = QLabel("Archivo Excel: ninguno")
        self.summary_label = QLabel("Registros: 0 | Errores de validación: 0")
        self.select_button = QPushButton("Seleccionar archivo Excel")
        self.select_button.clicked.connect(self.select_excel)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["Número de persona", "Campos solicitados", "Estado"]
        )
        self.table.setSortingEnabled(True)

        layout.addWidget(self.status_label)
        layout.addWidget(self.file_label)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.select_button)
        layout.addWidget(self.table)
        self.setCentralWidget(central)

    @Slot()
    def select_excel(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo Excel",
            str(ROOT_DIR / "data"),
            "Excel (*.xlsx)",
        )
        if not path:
            return
        self.load_excel(Path(path))

    def load_excel(self, path: Path) -> None:
        try:
            updates, errors = validate_file(
                path, ROOT_DIR / "config" / "catalogs.yaml"
            )
        except Exception as error:
            QMessageBox.critical(self, "Error de validación", str(error))
            return

        error_by_person = {
            error.split(":", 1)[0] for error in errors if ":" in error
        }
        self.file_label.setText(f"Archivo Excel: {path}")
        self.summary_label.setText(
            f"Registros: {len(updates)} | Errores de validación: {len(errors)}"
        )
        self.table.setRowCount(len(updates))
        for row, update in enumerate(updates):
            self.table.setItem(row, 0, QTableWidgetItem(update.person_number))
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(", ".join(update.requested_changes()) or "Ninguno"),
            )
            status = "ERROR_VALIDACION" if update.person_number in error_by_person else "VALIDADO"
            self.table.setItem(row, 2, QTableWidgetItem(status))
        if errors:
            QMessageBox.warning(
                self,
                "Validación completada con errores",
                "\n".join(errors[:20]),
            )


def create_window() -> MainWindow:
    settings.prepare_directories()
    return MainWindow()
