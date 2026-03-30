from collections.abc import Iterable
from dataclasses import asdict, fields
import json
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, PatternFill

from data_structures import Event, EventID, InputData, Seeker, Solution
from generators import generate_random_ranking
from hacks import FrozenDict, freeze_dict


class Color:
    WHITE = "FFFFFF"

    EVENT_HEADER = "000050"
    SEEKERS_FROM_BW_HEADER = "400080"
    SEEKERS_NOT_FROM_BW_HEADER = "004080"

    SUCCESS = "008000"
    FAILURE = "C80000"
    UNCHECKED_FROM_BW = "CCAAFF"
    UNCHECKED_NOT_FROM_BW = "AACCFF"


class XLSX:
    FIRST_INDEX = 1
    SEEKERS_SHEET_NAME = "data--seekers"
    EVENTS_SHEET_NAME = "data--events"
    RANDOM_RANKING_SHEET_NAME = "data--random-ranking"
    LOG_SHEET_NAME = "log"

    FROM_BW_STRING = "Baden-Württemberger*in"
    NOT_FROM_BW_STRING = " "

    @staticmethod
    def as_rows( # Only allows Events to prevent confusing rows and columns.
            events: Iterable[Event],
            number_of_header_rows: int = 1
        ) -> dict[Event, str]:

        rows: dict[Event, str] = dict()
        offset = XLSX.FIRST_INDEX + number_of_header_rows
        for i, event in enumerate(events, offset):
            rows[event] = str(i)

        return rows

    @staticmethod
    def as_columns( # Only allows Seekers to prevent confusing rows and columns.
            seekers: Iterable[Seeker],
            number_of_header_columns: int=1
        ) -> dict[Seeker, str]:

        columns: dict[Seeker, str] = dict()
        offset = XLSX.FIRST_INDEX + number_of_header_columns
        for i, seeker in enumerate(seekers, offset):
            columns[seeker] = get_column_letter(i)

        return columns

    @staticmethod
    def get_new_workbook(first_sheet_name: str) -> Workbook:
        xlsx = Workbook()
        if len(xlsx.worksheets) > 0: # should always be True after creation
            first_sheet = xlsx.worksheets[0]
        else:
            first_sheet = xlsx.create_sheet()
        first_sheet.title = first_sheet_name

        first_sheet.append([
            "Feel free to write or delete something here!"
        ])
        first_sheet.append([
            "This sheet is not read, overwritten or needed by the computer."
        ])
        first_sheet.append([
            "Switch sheets by pressing STRG + (SHIFT) + TAB."
        ])
        return xlsx

class XLSXWriter:
    @staticmethod
    def add_log_file_to_xlsx(log_file_path: Path, xlsx: Workbook):
        sheet = xlsx.create_sheet(XLSX.LOG_SHEET_NAME)
        with open(log_file_path, "r") as file:
            for line in file.readlines():
                sheet.append([line])
        return xlsx

    @staticmethod
    def add_data_to_xlsx(data: InputData, xlsx: Workbook):
        XLSXWriter._add_events(data.events, xlsx)
        XLSXWriter._add_seekers(data.seekers, xlsx)
        XLSXWriter._add_random_ranking(data, xlsx)
    
    @staticmethod
    def _add_events(events: tuple[Event, ...], xlsx: Workbook):
        sheet = xlsx.create_sheet(XLSX.EVENTS_SHEET_NAME)
        field_names = [field.name for field in fields(Event)]

        for column_index, field_name in enumerate(field_names, XLSX.FIRST_INDEX):
            column = get_column_letter(column_index)
            sheet[column + "1"] = field_name
            for event, row in XLSX.as_rows(events).items():
                sheet[column + row] = json.dumps(getattr(event, field_name))

    @staticmethod
    def _add_seekers(seekers: tuple[Seeker, ...], xlsx: Workbook):
        sheet = xlsx.create_sheet(XLSX.SEEKERS_SHEET_NAME)
        field_names = [field.name for field in fields(Seeker)]
    
        for row_index, field_name in enumerate(field_names, XLSX.FIRST_INDEX):
            row = str(row_index)
            sheet["A" + row] = field_name
            for seeker, column in XLSX.as_columns(seekers).items():
                if field_name == "wishes":
                    wishes = tuple(event.id for events in seeker.wishes for event in events)
                    value = json.dumps(wishes)
                else:
                    value = json.dumps(getattr(seeker, field_name))
                sheet[column+row] = value

    @staticmethod
    def _add_random_ranking(data: InputData, xlsx: Workbook):
        sheet = xlsx.create_sheet(XLSX.RANDOM_RANKING_SHEET_NAME)

        for event, row in XLSX.as_rows(data.events).items():
            for seeker, column in XLSX.as_columns(data.seekers).items():
                sheet[column+row] = json.dumps(data.random_ranking[event][seeker])

class XLSXReader:
    @staticmethod
    def read_from_xlsx(xlsx_path: Path) -> InputData:
        xlsx = load_workbook(xlsx_path)
        events = XLSXReader._get_events(xlsx)
        seekers = XLSXReader._get_seekers(xlsx, freeze_dict({e.id: e for e in events}))
        return InputData(
            name = xlsx_path.stem,
            events = events,
            seekers = seekers,
            random_ranking=XLSXReader._get_random_ranking(xlsx, events, seekers)
        )

    @staticmethod
    def _get_events(xlsx: Workbook) -> tuple[Event, ...]:
        sheet = xlsx[XLSX.EVENTS_SHEET_NAME]
        rows = sheet.iter_rows(values_only=True)
        field_names = [str(k) for k in next(rows)]
        events_as_dicts: list[dict[str, Any]] = list()
        for row in rows:
            schulung_as_dict = XLSXReader._get_as_dict(row, field_names)
            events_as_dicts.append(schulung_as_dict)
        return tuple([Event(**d) for d in events_as_dicts])
    
    @staticmethod
    def _get_seekers(xlsx: Workbook, events_by_id: FrozenDict[EventID, Event]) -> tuple[Seeker, ...]:
        sheet = xlsx[XLSX.SEEKERS_SHEET_NAME]
        columns = sheet.iter_cols(values_only=True)
        field_names = [str(k) for k in next(columns)]
        seekers_as_dicts: list[dict[str, Any]] = list()
        for column in columns:
            julei_as_dict = XLSXReader._get_as_dict(column, field_names)
            seekers_as_dicts.append(julei_as_dict)
        for seeker_as_dict in seekers_as_dicts:
            seeker_as_dict["wishes"] = tuple(events_by_id[e_id] for e_ids in seeker_as_dict["wishes"] for e_id in e_ids)

        return tuple([Seeker(**d) for d in seekers_as_dicts])

    @staticmethod
    def _get_random_ranking(
            xlsx: Workbook,
            events: Iterable[Event],
            seekers: Iterable[Seeker]
        ) -> FrozenDict[Event, FrozenDict[Seeker, int]]:
        if XLSX.RANDOM_RANKING_SHEET_NAME not in xlsx.sheetnames:
            return generate_random_ranking(events, list(seekers))

        sheet = xlsx[XLSX.RANDOM_RANKING_SHEET_NAME]
        random_ranking: dict[Event, FrozenDict[Seeker, int]] = dict()

        for event, row in XLSX.as_rows(events).items():
            one_random_ranking: dict[Seeker, int] = dict()
            for seeker, column in XLSX.as_columns(seekers).items():
                one_random_ranking[seeker] = int(sheet[column+row].value)
            random_ranking[event] = freeze_dict(one_random_ranking)

        return freeze_dict(random_ranking)

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
    def add_plot_to_xlsx(xlsx: Workbook, solution: Solution):
        rows = XLSX.as_rows(solution.parameters.events)
        columns = XLSX.as_columns(solution.parameters.seekers)
        sheet: Worksheet = xlsx.create_sheet(f"allocation")

        for column in ["A"] + list(columns.values()):
            sheet.column_dimensions[column].width = XLSXPlotter.COLUMN_WIDTH

        XLSXPlotter._add_headers(rows, columns, sheet)
        XLSXPlotter._write_wishes(rows, columns, sheet, solution)


    @staticmethod
    def _add_headers(rows: dict[Event, str], columns: dict[Seeker, str], sheet: Worksheet):
        sheet["A1"].fill = PatternFill("solid", Color.EVENT_HEADER)

        for event, row in rows.items():
            sheet["A"+row] = json.dumps(asdict(event))
            sheet["A"+row].font = Font(bold=True, color=Color.WHITE)
            sheet["A"+row].fill = PatternFill("solid", Color.EVENT_HEADER)
            sheet["A"+row].alignment = Alignment(horizontal='center')

        for seeker, column in columns.items():
            sheet[column+"1"].font = Font(bold=True, color=Color.WHITE)
            sheet[column+"1"] = json.dumps(asdict(seeker))
            if seeker.from_bw:
               sheet[column+"1"].fill = PatternFill("solid", Color.SEEKERS_FROM_BW_HEADER)
            else:
               sheet[column+"1"].fill = PatternFill("solid", Color.SEEKERS_NOT_FROM_BW_HEADER)

    @staticmethod
    def _write_wishes(
            rows: dict[Event, str],
            columns: dict[Seeker, str],
            sheet: Worksheet,
            solution: Solution
        ):
        for seeker, wishes in solution.total_wishes.items():
            column = columns[seeker]
            for priority, event in enumerate(wishes, 1):
                row = rows[event]
                sheet[column+row] = priority
                sheet[column+row].font = Font(color=Color.WHITE)
                sheet[column+row].alignment = Alignment(horizontal='center')
                sheet[column+row].fill = PatternFill("solid", Color.FAILURE)

        for seeker, wishes in solution.accepted_wishes.items():
            column = columns[seeker]
            for priority, event in enumerate(wishes, 1):
                row = rows[event]
                sheet[column+row].fill = PatternFill("solid", Color.SUCCESS)
        
        for seeker, wishes in solution.unchecked_wishes.items():
            column = columns[seeker]
            for priority, event in enumerate(wishes, 1):
                row = rows[event]
                if seeker.from_bw:
                    sheet[column+row].fill = PatternFill("solid", Color.UNCHECKED_FROM_BW)
                else:
                    sheet[column+row].fill = PatternFill("solid", Color.UNCHECKED_NOT_FROM_BW)
