from collections.abc import Iterable
from dataclasses import fields
import json
from os import makedirs
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, PatternFill

from data_structures import JuLei, Schulung, CompleteData, State

class XLSX:
    FIRST_INDEX = 1
    JULEI_SHEET_NAME = "data--juleis"
    SCHULUNGEN_SHEET_NAME = "data--schulungen"

    FROM_BW_STRING = "Baden-Württemberger*in"
    NOT_FROM_BW_STRING = " "

    @staticmethod
    def as_rows( # Only allows Schulungen to prevent confusing rows and columns.
            schulungen: Iterable[Schulung],
            number_of_header_rows: int=1
        ) -> dict[Schulung, str]:

        rows: dict[Schulung, str] = dict()
        offset = XLSX.FIRST_INDEX + number_of_header_rows
        for i, schulung in enumerate(schulungen, offset):
            rows[schulung] = str(i)

        return rows

    @staticmethod
    def as_columns( # Only allows JuLeis to prevent confusing rows and columns.
            juleis: Iterable[JuLei],
            number_of_header_columns: int=1
        ) -> dict[JuLei, str]:

        columns: dict[JuLei, str] = dict()
        offset = XLSX.FIRST_INDEX + number_of_header_columns
        for i, julei in enumerate(juleis, offset):
            columns[julei] = get_column_letter(i)

        return columns

    @staticmethod
    def get_new_workbook(data: CompleteData) -> Workbook:
        xlsx = Workbook()
        if len(xlsx.worksheets) > 0: # should always be True after creation
            first_sheet = xlsx.worksheets[0]
        else:
            first_sheet = xlsx.create_sheet()
    
        first_sheet.title = data.name
        first_sheet.append([
            "Feel free to write or delete something here!",
            "This sheet is not read, overwritten or needed by the computer.",
            "Switch sheets by pressing STRG + (SHIFT) + TAB."
        ])

        print(
            f"  Allocates {len(data.juleis)} JuLeis with {data.number_of_wishes} wishes",
            f"  to {data.number_of_slots} Slots in {len(data.schulungen)} Schulungen.",
            f"  On average, each julei has {data.number_of_wishes // len(data.juleis)} wishes.",
            sep="\n"
        )

        return xlsx

class Color:
    WHITE = "FFFFFF"

    SCHULUNG_HEADER = "000050"
    JULEI_FROM_BW_HEADER = "400080"
    JULEI_NOT_FROM_BW_HEADER = "004080"

    HIGHLIGHT = "FA00FA"
    SUCCESS = "008000"
    FAILURE = "800020"

    WISH_BRIGHTNESS = (0, 50, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170)
    WISH_OF_ALLOCATED_JULEI_BASE_RGB = (0, 80, 40)
    WISH_FROM_BW_BASE_RGB = (40, 0, 80)
    WISH_NOT_FROM_BW_BASE_RGB = (0, 40, 80)

    @staticmethod
    def wish(brightness_level: int | None, allocated: bool, from_bw: bool) -> str:
        maximum_brightness_level = len(Color.WISH_BRIGHTNESS)-1

        if brightness_level is None:
            brightness_level = maximum_brightness_level
        if brightness_level > maximum_brightness_level:
            brightness_level = maximum_brightness_level
        if brightness_level < 0:
            brightness_level = 0

        brightness = Color.WISH_BRIGHTNESS[brightness_level]
        if allocated:
            base = Color.WISH_OF_ALLOCATED_JULEI_BASE_RGB
        elif from_bw:
            base = Color.WISH_FROM_BW_BASE_RGB
        else:
            base = Color.WISH_NOT_FROM_BW_BASE_RGB

        rgb: list[int] = list()
        for channel in base:
            rgb.append(max(0, min(255, channel+brightness)))

        return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

class XLSXWriter:
    @staticmethod
    def get_minimal_xlsx(data: CompleteData, output_directory: Path | None=None) -> Workbook:
        xlsx = XLSX.get_new_workbook(data)
        XLSXWriter._add_schulungen(data.schulungen, xlsx)
        XLSXWriter._add_juleis(data.juleis, xlsx)
        if output_directory:
           makedirs(output_directory, exist_ok=True)
           xlsx.save(output_directory/f"{data.name}.xlsx")
        return xlsx
    
    @staticmethod
    def _add_schulungen(schulungen: tuple[Schulung, ...], xlsx: Workbook):
        sheet = xlsx.create_sheet(XLSX.SCHULUNGEN_SHEET_NAME)
        field_names = [field.name for field in fields(Schulung)]
    
        for column_index, field_name in enumerate(field_names, XLSX.FIRST_INDEX):
            column = get_column_letter(column_index)
            sheet[column + "1"] = field_name
            for schulung, row in XLSX.as_rows(schulungen).items():
                sheet[column + row] = json.dumps(getattr(schulung, field_name))

    @staticmethod
    def _add_juleis(juleis: tuple[JuLei, ...], xlsx: Workbook):
        sheet = xlsx.create_sheet(XLSX.JULEI_SHEET_NAME)
        field_names = [field.name for field in fields(JuLei)]
    
        for row_index, field_name in enumerate(field_names, XLSX.FIRST_INDEX):
            row = str(row_index)
            sheet["A" + row] = field_name
            for julei, column in XLSX.as_columns(juleis).items():
                sheet[column+row] = json.dumps(getattr(julei, field_name))
    
class XLSXReader:
    @staticmethod
    def read_from_xlsx(xlsx_path: Path) -> CompleteData:
        xlsx = load_workbook(xlsx_path)
        return CompleteData(
            name = xlsx_path.stem,
            schulungen = XLSXReader._get_schulungen(xlsx),
            juleis = XLSXReader._get_juleis(xlsx)
        )
    
    @staticmethod
    def _get_schulungen(xlsx: Workbook) -> tuple[Schulung, ...]:
        sheet = xlsx[XLSX.SCHULUNGEN_SHEET_NAME]
        rows = sheet.iter_rows(values_only=True)
        field_names = [str(k) for k in next(rows)]
        schulungen_as_dicts: list[dict[str, Any]] = list()
        for row in rows:
            schulung_as_dict = XLSXReader._get_as_dict(row, field_names)
            schulungen_as_dicts.append(schulung_as_dict)
        return tuple([Schulung(**d) for d in schulungen_as_dicts])
    
    @staticmethod
    def _get_juleis(xlsx: Workbook) -> tuple[JuLei, ...]:
        sheet = xlsx[XLSX.JULEI_SHEET_NAME]
        columns = sheet.iter_cols(values_only=True)
        field_names = [str(k) for k in next(columns)]
        juleis_as_dicts: list[dict[str, Any]] = list()
        for column in columns:
            julei_as_dict = XLSXReader._get_as_dict(column, field_names)
            juleis_as_dicts.append(julei_as_dict)
        return tuple([JuLei(**d) for d in juleis_as_dicts])
    
    @staticmethod
    def _get_as_dict(cells: tuple[Any, ...], field_names: Iterable[str]) -> dict[str, Any]:
        as_dict: dict[str, Any] = dict()
        for i, field_name in enumerate(field_names):
            as_dict[field_name] = json.loads(str(cells[i]))
        return XLSXReader.convert_lists_back_to_tuples(as_dict)

    @staticmethod
    def convert_lists_back_to_tuples(
            dict_from_json: dict[str, Any]
        ) -> dict[str, Any]:
        """JSON does not know tuples and converts them to lists."""
        for key, value in dict_from_json.items():
            if isinstance(value, list):
                dict_from_json[key] = tuple(value) # pyright: ignore[reportUnknownArgumentType]
        return dict_from_json


class XLSXPlotter:
    COLUMN_WIDTH = 2.5
    @staticmethod
    def add_plot_of_state(
            xlsx: Workbook,
            state: State,
            previous_allocations: dict[Schulung, list[JuLei]]
        ) -> Workbook:
        rows = XLSX.as_rows(state.parameters.schulungen)
        columns = XLSX.as_columns(state.parameters.juleis)
        sheet: Worksheet = xlsx.create_sheet(f"{state.time:.6f}")

        for column in ["A"] + list(columns.values()):
            sheet.column_dimensions[column].width = XLSXPlotter.COLUMN_WIDTH

        XLSXPlotter._add_headers(rows, columns, sheet)
        XLSXPlotter._add_values(
            rows,
            columns,
            sheet,
            state,
            previous_allocations
        )
        return xlsx

    @staticmethod
    def _add_headers(rows: dict[Schulung, str], columns: dict[JuLei, str], sheet: Worksheet):
        sheet["A1"].fill = PatternFill("solid", Color.SCHULUNG_HEADER)

        for schulung, row in rows.items():
            sheet["A"+row] = schulung.capacity
            sheet["A"+row].font = Font(bold=True, color=Color.WHITE)
            sheet["A"+row].fill = PatternFill("solid", Color.SCHULUNG_HEADER)
            sheet["A"+row].alignment = Alignment(horizontal='center')

        for julei, column in columns.items():
            sheet[column+"1"].font = Font(bold=True, color=Color.WHITE)
            if julei.from_bw:
               sheet[column+"1"] = XLSX.FROM_BW_STRING
               sheet[column+"1"].fill = PatternFill("solid", Color.JULEI_FROM_BW_HEADER)
            else:
               sheet[column+"1"] = XLSX.NOT_FROM_BW_STRING
               sheet[column+"1"].fill = PatternFill("solid", Color.JULEI_NOT_FROM_BW_HEADER)
    
    @staticmethod
    def _add_values(
            rows: dict[Schulung, str],
            columns: dict[JuLei, str],
            sheet: Worksheet,
            state: State,
            allocations_of_previous_state: dict[Schulung, list[JuLei]],
        ):
        # Having this as a function prevents that
        # the @property-methods of State are evaluated more then once.
        for julei, column in columns.items():
            for schulung, row in rows.items():

                if schulung not in state.parameters.wishes[julei]:
                    priority = None
                else:
                    priority = state.parameters.wishes[julei].index(schulung)
                    sheet[column+row] = priority + 1

                if (julei in state.allocations[schulung] and
                    schulung in state.overcrowded_schulungen):
                    color = Color.HIGHLIGHT
                elif julei in state.allocations[schulung]:
                    color = Color.SUCCESS
                elif julei in allocations_of_previous_state[schulung]:
                    color = Color.FAILURE
                elif state.is_allocated(julei):
                    color = Color.wish(priority, True, julei.from_bw)
                elif state.can_not_be_allocated(julei):
                    color = Color.wish(priority, True, julei.from_bw)
                else:
                    color = Color.wish(priority, False, julei.from_bw)

                sheet[column+row].font = Font(color=Color.WHITE)
                sheet[column+row].alignment = Alignment(horizontal='center')
                sheet[column+row].fill = PatternFill("solid", color)

    @staticmethod
    def _color_cells(
            rows: dict[Schulung, str],
            columns: dict[JuLei, str],
            sheet: Worksheet,
            schulungen: Iterable[Schulung],
            juleis: list[JuLei],
            color: str
        ):
        for row in (rows[s] for s in schulungen):
            for column in (columns[j] for j in juleis):
                sheet[column+row].fill = PatternFill("solid", color)
