"""
Not using dataframes-image because it does not allow to set edgecolors and fonts
and is tidious to work with.
Not using images because they take long to generate and are not readable.
"""
from os import makedirs
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.utils import get_column_letter

from config import FIRST_XLSX_SHEET, COLUMN_WIDTH
from config import FIRST_INDEX_IN_XLSX, FROM_BW_STRING
from config import FULL_SCHULUNG_COLOR, WISH_FROM_BW_COLOR, WISH_NOT_FROM_BW_COLOR
from config import ALLOCATION_COLOR, ALLOCATED_JULEI_COLOR
from data_containers import Problem, JuLei

def _draw_first_row(p: Problem, table: Any):
    for julei, column_letter in p.columns_in_xlsx.items():
        cell_index = column_letter + str(FIRST_INDEX_IN_XLSX)
        table[cell_index].font = Font(bold=True)
        if p.from_bw[julei]:
            table[cell_index] = FROM_BW_STRING
        else:
            table[cell_index] = " "
        if not (p.get_allocation(julei) is None):
            table[cell_index].fill = PatternFill(start_color=ALLOCATED_JULEI_COLOR, fill_type="solid")

def _draw_first_column(p: Problem, table: Any):
    for schulung, row_index in p.rows_in_xlsx.items():
        cell_index = get_column_letter(FIRST_INDEX_IN_XLSX) + row_index
        table[cell_index].font = Font(bold=True)
        table[cell_index] = p.capacity[schulung]
        if p.is_full(schulung):
            table[cell_index].fill = PatternFill(start_color=FULL_SCHULUNG_COLOR, fill_type="solid")

def _draw_participants(p: Problem, table: Any):
    for schulung, juleis in p.participants.items():
        for julei in juleis:
            cell_index = p.columns_in_xlsx[julei] + p.rows_in_xlsx[schulung]
            table[cell_index].fill = PatternFill(start_color=ALLOCATION_COLOR, fill_type="solid")

def _draw_column(p: Problem, table: Any, julei: JuLei):
    for priority, schulung in enumerate(p.remaining_wishes[julei]):
        cell_index = p.columns_in_xlsx[julei] + p.rows_in_xlsx[schulung]
        table[cell_index] = priority
        if priority == 0:
            if p.from_bw[julei]:
                table[cell_index].fill = PatternFill(start_color=WISH_FROM_BW_COLOR, fill_type="solid")
            else:
                table[cell_index].fill = PatternFill(start_color=WISH_NOT_FROM_BW_COLOR, fill_type="solid")

def save_to_xlsx(p: Problem, title: str, juleis: list[JuLei] | None=None):
    xlsx_file_path = p.output_directory/f"{p.name}.xlsx"
    xlsx_file = load_workbook(xlsx_file_path)
    table = xlsx_file.create_sheet(title)

    for column_letter in p.columns_in_xlsx.values():
        table.column_dimensions[column_letter].width = COLUMN_WIDTH

    _draw_first_row(p, table)
    _draw_first_column(p, table)
    _draw_participants(p, table)

    if not(juleis is None):
        for julei in juleis:
            _draw_column(p, table, julei)
    else:
        for julei in p.remaining_wishes.keys():
            _draw_column(p, table, julei)

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
