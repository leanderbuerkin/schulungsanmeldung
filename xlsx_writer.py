from collections.abc import Generator, Iterable
from functools import partial
from os import makedirs
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.worksheet import Worksheet

from data import Data, JuLei, Schulung
from participants_lists_generator import get_steps_of_getting_participants_lists
from xlsx_config import COLUMN_WIDTH, FROM_BW_STRING, NOT_FROM_BW_STRING, Colors, get_new_workbook, get_sheet_generator
from xlsx_config import index_as_columns, index_as_rows
from xlsx_minimal_writer import add_minimal_xlsx

def _draw_headers(rows: dict[Schulung, str], columns: dict[JuLei, str], sheet: Worksheet):
    for column in ["A"] + list(columns.values()):
        sheet.column_dimensions[column].width = COLUMN_WIDTH
    sheet["A1"].fill = PatternFill("solid", Colors.SCHULUNG_HEADER)
    for schulung, row in rows.items():
        sheet["A"+row] = schulung.capacity
        sheet["A"+row].font = Font(bold=True, color=Colors.WHITE)
        sheet["A"+row].fill = PatternFill("solid", Colors.SCHULUNG_HEADER)
        sheet["A"+row].alignment = Alignment(horizontal='center')
    for julei, column in columns.items():
        sheet[column+"1"].font = Font(bold=True, color=Colors.WHITE)
        if julei.from_bw:
           sheet[column+"1"] = FROM_BW_STRING
           sheet[column+"1"].fill = PatternFill("solid", Colors.JULEI_FROM_BW_HEADER)
        else:
           sheet[column+"1"] = NOT_FROM_BW_STRING
           sheet[column+"1"].fill = PatternFill("solid", Colors.JULEI_NOT_FROM_BW_HEADER)

def _draw_wishes(wishes: dict[JuLei, list[Schulung]],
        rows: dict[Schulung, str], columns: dict[JuLei, str], sheet: Worksheet):
    for julei, column in columns.items():
        for priority, row in enumerate(rows[s] for s in wishes[julei]):
            sheet[column+row] = priority + 1
            sheet[column+row].font = Font(color=Colors.WHITE)
            sheet[column+row].alignment = Alignment(horizontal='center')
            sheet[column+row].fill = PatternFill("solid", Colors.wish(priority, julei.from_bw))

def _color_cells(
        rows: dict[Schulung, str], columns: dict[JuLei, str],
        schulungen: Iterable[Schulung], juleis: Iterable[JuLei],
        color: str, sheet: Worksheet,
    ):
    for row in (rows[s] for s in schulungen):
        for column in (columns[j] for j in juleis):
            sheet[column+row].fill = PatternFill("solid", color)

def _draw_process_step(
        sheet_generator: Generator[Worksheet],
        rows: dict[Schulung, str], columns: dict[JuLei, str],
        participants: dict[Schulung, list[JuLei]],
        updated_schulung: Schulung | None, rejected_julei: JuLei | None
    ):
    if updated_schulung is None:
        return
    color_cells = partial(_color_cells, rows, columns)
    accepted_juleis = participants[updated_schulung]
    if rejected_julei:
        color_cells([updated_schulung], accepted_juleis + [rejected_julei],
                    Colors.HIGHLIGHTED_WISH, next(sheet_generator))
    sheet = next(sheet_generator)
    color_cells([updated_schulung], accepted_juleis, Colors.GRANTED_WISH, sheet)
    if rejected_julei:
        color_cells([updated_schulung], [rejected_julei], Colors.REJECTED_WISH, sheet)

def get_xlsx(data: Data, output_directory: Path | None=None) -> Workbook:
    xlsx = get_new_workbook(data.name)
    rows = index_as_rows(data.schulungen)
    columns = index_as_columns(data.juleis)
    sheet_generator = get_sheet_generator(xlsx)
    sheet = next(sheet_generator)
    draw_process_step = partial(_draw_process_step, sheet_generator, rows, columns)

    _draw_headers(rows, columns, sheet)
    _draw_wishes(data.get_wishes_of_juleis(), rows, columns, sheet)

    for process_step in get_steps_of_getting_participants_lists(data):
        draw_process_step(*process_step)

    xlsx = add_minimal_xlsx(xlsx, data)

    if output_directory:
        makedirs(output_directory, exist_ok=True)
        xlsx.save(output_directory/f"{data.name}.xlsx")
    return xlsx

"""
from time import gmtime, strftime, time

from config import data_DIRECTORY
from data_containers import Problem
from file_saver import save_to_xlsx
from random_problem_generator import generate_random_problem
from allocator import allocate

def print_stats(p: Problem, start_time: float, work_worst_case: int, work_expected: int):
    total_processing_time = time()-start_time
    work_done = p.number_of_checked_allocations
    width_work_worst_case = len(str(work_worst_case))
    if work_done == 0:
        return
    print("-----------")
    print(f"Worst Case: {work_done} of {work_worst_case} " +
        f"({work_done*100/work_worst_case:.2f} %) in {strftime("%H:%M:%S", gmtime(total_processing_time))} " +
        f"-> Remaining time: {strftime("%H:%M:%S", gmtime((total_processing_time/work_done) * work_worst_case - total_processing_time))}"
    )
    print(f"Expected:   {work_done} of {work_expected:>{width_work_worst_case}} " +
        f"({work_done*100/work_expected:.2f} %) in {strftime("%H:%M:%S", gmtime(total_processing_time))} " +
        f"-> Remaining time: {strftime("%H:%M:%S", gmtime((total_processing_time/work_done) * work_expected - total_processing_time))}"
    )

problem = generate_random_problem(data_DIRECTORY, 50, 200, (8, 12), 80, (1, 5))
work_worst_case = problem.worst_case_final_number_of_checked_allocations
work_expected = problem.expected_final_number_of_checked_allocations
start_time = time()

time_before_allocation = time()
for julei in allocate(problem):
    print(f"Allocation took     {time() - time_before_allocation:.6f} s.")

    time_before_saving = time()
    save_to_xlsx(
        problem,
        f"{time()-start_time:.2f} s",
        [julei]
    )

    print(f"Saving to xlsx took {time() - time_before_saving:.6f} s.")
    print_stats(problem, start_time, work_worst_case, work_expected)

    time_before_allocation = time()

total_processing_time = time()-start_time
save_to_xlsx(problem, f"{total_processing_time:.2f} s")
print("Saving result...")
problem.save_to_file()
print("Finished")
"""