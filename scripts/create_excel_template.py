from pathlib import Path

from openpyxl import Workbook

from models.employee import EMPLOYEE_FIELDS


def main() -> None:
    output = Path("data") / "plantilla_empleados.xlsx"
    output.parent.mkdir(exist_ok=True)
    workbook = Workbook()
    workbook.active.append(["PersonNumber", *EMPLOYEE_FIELDS])
    workbook.save(output)
    print(f"Plantilla creada: {output}")


if __name__ == "__main__":
    main()
