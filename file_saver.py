"""
Not using dataframes-image because it does not allow to set edgecolors and fonts
and is tidious to work with.
Not using images because they take long to generate and are not readable
"""
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

from config import DATA_DIRECTORY, STRING_FOR_ALLOCATIONS
from config import FROM_BW_STRING, NOT_FROM_BW_STRING
from data_containers import Problem

FIRST_INDEX_IN_XLSX = 1
NUMBER_OF_HEADER_COLUMNS = 1
NUMBER_OF_HEADER_ROWS = 1
FIRST_CONTENT_COLUMN_INDEX = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_COLUMNS
FIRST_CONTENT_ROW_INDEX = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_ROWS

WIDTH_OF_ONE_DIGIT = 1.5  # guess
TRANSPARENCY_STEPS = 50
TRANSPARENCY_LEVELS = 3

COLOR_JULEI_FROM_BW = "400080"
def color_wish_from_bw(i: int) -> str:
    rgb = (min(215, 40+50*i), min(175, 50*i), min(255, 80+50*i))
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

COLOR_JULEI_NOT_FROM_BW = "004080"
def color_wish_not_from_bw(i: int) -> str:
    rgb = (min(175, 50*i), min(215, 40+50*i), min(255, 80+50*i))
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def save_to_new_xlsx(p: Problem, title: str) -> Path:
    xlsx_file_path = DATA_DIRECTORY/f"{p.name}.xlsx"
    Workbook().save(xlsx_file_path)
    return save_to_xlsx(p, xlsx_file_path, title)

def get_cell_index(schulung_index: int, julei_index: int) -> str:
    column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung_index)
    row_index = FIRST_CONTENT_ROW_INDEX + julei_index
    return column_letter + str(row_index)

def draw_top_left_cell(table: Any) -> None:
    table["A1"] = "Plätze:"
    table["A1"].fill = PatternFill(start_color="000050", fill_type="solid")
    table["A1"].font = Font(bold=True, color="FFFFFF")
    return table

def draw_first_row(p: Problem, table: Any) -> Any:
    for schulung_index, schulung in enumerate(p.schulungen):
        column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung_index)
        cell_index = column_letter + str(FIRST_INDEX_IN_XLSX)
        table[cell_index] = str(schulung.capacity)
        table[cell_index].fill = PatternFill(start_color="000050", fill_type="solid")
        table[cell_index].font = Font(bold=True, color="FFFFFF")
    return table

def draw_first_column(p: Problem, table: Any) -> Any:
    for julei_index, julei in enumerate(p.juleis):
        column_letter = get_column_letter(FIRST_INDEX_IN_XLSX)
        row_index = FIRST_CONTENT_ROW_INDEX + julei_index
        cell_index = column_letter + str(row_index)
        if julei.from_bw:
            table[cell_index] = FROM_BW_STRING
            table[cell_index].fill = PatternFill(start_color=COLOR_JULEI_FROM_BW, fill_type="solid")
        else:
            table[cell_index] = NOT_FROM_BW_STRING
            table[cell_index].fill = PatternFill(start_color=COLOR_JULEI_NOT_FROM_BW, fill_type="solid")
        table[cell_index].font = Font(bold=True, color="FFFFFF")
    return table

def draw_allocations(p: Problem, table: Any) -> Any:
    for schulung_index, schulung in enumerate(p.schulungen):
        for julei_index in (p.juleis.index(j) for j in schulung.participants):
            i = get_cell_index(schulung_index, julei_index)
            table[i] = STRING_FOR_ALLOCATIONS
            table[i].alignment = Alignment(horizontal='center', vertical='center')
            table[i].fill = PatternFill(start_color="00FF00", fill_type="solid")

def draw_wishes(p: Problem, table: Any) -> Any:
    for julei_index, julei in enumerate(p.juleis):
        for priority, schulung_index in enumerate(julei.wishes):
            i = get_cell_index(schulung_index, julei_index)
            table[i] = priority
            table[i].alignment = Alignment(horizontal='center', vertical='center')
            if p.julei_is_allocated(julei):
                table[i].fill = PatternFill(start_color="BBFFBB", fill_type="solid")
            elif julei.from_bw:
                table[i].fill = PatternFill(start_color=color_wish_from_bw(priority), fill_type="solid")
                table[i].font = Font(color="FFFFFF")
            else:
                table[i].fill = PatternFill(start_color=color_wish_not_from_bw(priority), fill_type="solid")
                table[i].font = Font(color="FFFFFF")
    return table

def save_to_xlsx(p: Problem, xlsx_file_path: Path, title: str) -> Path:
    xlsx_file = load_workbook(xlsx_file_path)
    table = xlsx_file.create_sheet(title)

    for schulung_index in range(len(p.schulungen)):
        column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung_index)
        table.column_dimensions[column_letter].width = 2*WIDTH_OF_ONE_DIGIT

    table = draw_top_left_cell(table)
    table = draw_first_row(p, table)
    table = draw_first_column(p, table)
    table = draw_wishes(p, table)
    table = draw_allocations(p, table)

    xlsx_file.save(xlsx_file_path)
    return xlsx_file_path
