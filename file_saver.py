"""
Not using dataframes-image because it does not allow to set edgecolors and fonts
and is tidious to work with.
Not using images because they take long to generate and are not readable
"""
from os import makedirs
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

from config import FIRST_XLSX_SHEET, WIDTH_OF_ONE_DIGIT
from config import FIRST_CONTENT_COLUMN_INDEX, FIRST_CONTENT_ROW_INDEX, FIRST_INDEX_IN_XLSX
from config import FROM_BW_STRING, NOT_FROM_BW_STRING, ALLOCATIONS_STRING
from config import TOP_ROW_COLOR, JULEI_FROM_BW_COLOR, JULEI_NOT_FROM_BW_COLOR
from config import WHITE, ALLOCATION_COLOR, WISH_FROM_ALLOCATED_JULEI_COLOR
from config import wish_from_bw_color, wish_not_from_bw_color
from data_containers import Problem, Schulung, JuLei

def _get_content_cell_index(schulung: Schulung, julei: JuLei) -> str:
    column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung.id)
    row_index = FIRST_CONTENT_ROW_INDEX + julei.id
    return column_letter + str(row_index)

def _draw_top_left_cell(table: Any):
    table["A1"] = "Plätze:"
    table["A1"].fill = PatternFill(start_color=TOP_ROW_COLOR, fill_type="solid")
    table["A1"].font = Font(bold=True, color="FFFFFF")

def _draw_first_row(p: Problem, table: Any):
    for schulung in p.schulungen.values():
        column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung.id)
        cell_index = column_letter + str(FIRST_INDEX_IN_XLSX)
        table[cell_index] = str(schulung.capacity)
        table[cell_index].fill = PatternFill(start_color=TOP_ROW_COLOR, fill_type="solid")
        table[cell_index].font = Font(bold=True, color="FFFFFF")

def _draw_first_column(p: Problem, table: Any):
    for julei in p.juleis.values():
        column_letter = get_column_letter(FIRST_INDEX_IN_XLSX)
        row_index = FIRST_CONTENT_ROW_INDEX + julei.id
        cell_index = column_letter + str(row_index)
        if julei.from_bw:
            table[cell_index] = FROM_BW_STRING
            table[cell_index].fill = PatternFill(start_color=JULEI_FROM_BW_COLOR, fill_type="solid")
        else:
            table[cell_index] = NOT_FROM_BW_STRING
            table[cell_index].fill = PatternFill(start_color=JULEI_NOT_FROM_BW_COLOR, fill_type="solid")
        table[cell_index].font = Font(bold=True, color="FFFFFF")

def _draw_allocations(p: Problem, table: Any):
    for schulungs_index, participants_ids in p.participants.items():
        for julei_index in participants_ids:
            i = _get_content_cell_index(p.schulungen[schulungs_index], p.juleis[julei_index])
            table[i] = ALLOCATIONS_STRING
            table[i].alignment = Alignment(horizontal='center', vertical='center')
            table[i].fill = PatternFill(start_color=ALLOCATION_COLOR, fill_type="solid")

def _draw_wishes(p: Problem, table: Any) -> Any:
    for julei in p.juleis.values():
        for priority, schulung_index in enumerate(julei.wishes):
            i = _get_content_cell_index(p.schulungen[schulung_index], julei)
            table[i] = priority
            table[i].alignment = Alignment(horizontal='center', vertical='center')
            if p.is_allocated(julei):
                table[i].fill = PatternFill(start_color=WISH_FROM_ALLOCATED_JULEI_COLOR, fill_type="solid")
            elif julei.from_bw:
                table[i].fill = PatternFill(start_color=wish_from_bw_color(priority), fill_type="solid")
                table[i].font = Font(color=WHITE)
            else:
                table[i].fill = PatternFill(start_color=wish_not_from_bw_color(priority), fill_type="solid")
                table[i].font = Font(color=WHITE)

def save_to_xlsx(p: Problem, title: str):
    print(title)
    xlsx_file_path = p.output_directory/f"{p.name}.xlsx"
    xlsx_file = load_workbook(xlsx_file_path)
    table = xlsx_file.create_sheet(title)

    for schulung_index in range(len(p.schulungen)):
        column_letter = get_column_letter(FIRST_CONTENT_COLUMN_INDEX + schulung_index)
        table.column_dimensions[column_letter].width = 2*WIDTH_OF_ONE_DIGIT

    _draw_top_left_cell(table)
    _draw_first_row(p, table)
    _draw_first_column(p, table)
    _draw_wishes(p, table)
    _draw_allocations(p, table)

    xlsx_file.save(xlsx_file_path)

def save_to_new_xlsx(p: Problem):
    makedirs(p.output_directory, exist_ok=True)
    xlsx_file_path = p.output_directory/f"{p.name}.xlsx"
    Workbook().save(xlsx_file_path)

    save_to_xlsx(p, FIRST_XLSX_SHEET)

    # delete the default sheet
    xlsx_file = load_workbook(xlsx_file_path)
    for sheetname in xlsx_file.sheetnames:
        if sheetname != FIRST_XLSX_SHEET:
            del xlsx_file[sheetname]
    xlsx_file.save(xlsx_file_path)
