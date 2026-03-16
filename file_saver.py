"""
Not using dataframes-image because it does not allow to set edgecolors and fonts
and is tidious to work with.
Not using images because they take long to generate and are not readable
"""
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

from config import DATA_DIRECTORY
from config import FROM_BW_STRING, NOT_FROM_BW_STRING, STRING_TO_MARK_ALLOCATIONS
from data_containers import JuLei, Problem
from logger import log_time

FIRST_INDEX_IN_XLSX = 1
NUMBER_OF_HEADER_COLUMNS = 1
NUMBER_OF_HEADER_ROWS = 1
FIRST_CONTENT_COLUMN_INDEX = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_COLUMNS
FIRST_CONTENT_ROW_INDEX = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_ROWS

WIDTH_OF_ONE_DIGIT = 1.5  # guess
TRANSPARENCY_STEPS = 50
TRANSPARENCY_LEVELS = 3

def _increase_transparency(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    rgb = (rgb[0] + TRANSPARENCY_STEPS, rgb[1] + TRANSPARENCY_STEPS, rgb[2] + TRANSPARENCY_STEPS)
    return min(255, rgb[0]), min(255, rgb[1]), min(255, rgb[2])

def _color(julei: JuLei, transparency: int | None=None) -> str:
    if julei.from_bw:
        rgb = (40, 0, 80)
    else:
        rgb = (0, 40, 80)
    if transparency is not None:
        rgb = _increase_transparency(rgb)
        for _ in range(min(TRANSPARENCY_LEVELS-1, transparency)):
            rgb = _increase_transparency(rgb)
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def save_to_new_xlsx(p: Problem, title: str) -> Path:
    xlsx_file_path = DATA_DIRECTORY/f"{p.name}.xlsx"
    Workbook().save(xlsx_file_path)
    return save_to_xlsx(p, xlsx_file_path, title)

def save_to_xlsx(p: Problem, xlsx_file_path: Path, title: str) -> Path:
    xlsx_file = load_workbook(xlsx_file_path)
    table = xlsx_file.create_sheet(title)

    table["A1"] = "Plätze:"
    table["A1"].fill = PatternFill(start_color="000050", fill_type="solid")
    table["A1"].font = Font(bold=True, color="FFFFFF")

    for schulung_index, capacity in enumerate(p.schulungen):
        column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung_index)
        table.column_dimensions[column_letter].width = 2*WIDTH_OF_ONE_DIGIT

        cell_index = column_letter + str(FIRST_INDEX_IN_XLSX)
        table[cell_index] = str(capacity)
        table[cell_index].fill = PatternFill(start_color="000050", fill_type="solid")
        table[cell_index].font = Font(bold=True, color="FFFFFF")


    for julei_index, julei in enumerate(p.juleis):
        column_letter = get_column_letter(FIRST_INDEX_IN_XLSX)
        row_index = FIRST_CONTENT_ROW_INDEX + julei_index

        cell_index = column_letter + str(row_index)
        if julei.from_bw:
            table[cell_index] = FROM_BW_STRING
            table[cell_index].fill = PatternFill(start_color=_color(julei), fill_type="solid")
            table[cell_index].font = Font(bold=True, color="FFFFFF")
        else:
            table[cell_index] = NOT_FROM_BW_STRING
            table[cell_index].fill = PatternFill(start_color=_color(julei), fill_type="solid")
            table[cell_index].font = Font(bold=True, color="FFFFFF")

        for priority, schulung_index in enumerate(julei.wishes):
            if schulung_index == julei.allocated:
                continue
            column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung_index)
            cell_index = column_letter + str(row_index)
            table[cell_index] = priority
            table[cell_index].alignment = Alignment(horizontal='center', vertical='center')
            if julei.allocated is None:
                table[cell_index].fill = PatternFill(start_color=_color(julei, priority), fill_type="solid")
                table[cell_index].font = Font(color="FFFFFF")
            else:
                table[cell_index].fill = PatternFill(start_color="BBFFBB", fill_type="solid")
                table[cell_index].font = Font(color="FFFFFF")

        if julei.allocated is not None:
            column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + julei.allocated)
            cell_index = column_letter + str(row_index)
            table[cell_index] = STRING_TO_MARK_ALLOCATIONS
            table[cell_index].fill = PatternFill(start_color="00FF00", fill_type="solid")
            table[cell_index].alignment = Alignment(horizontal='center', vertical='center')
            table[cell_index].font = Font(color="FFFFFF")

    xlsx_file.save(xlsx_file_path)
    log_time(f"saved_to_xlsx_problem_{p.name}")
    return xlsx_file_path
