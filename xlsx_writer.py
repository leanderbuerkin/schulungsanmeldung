from collections.abc import Iterable
from dataclasses import fields
from os import makedirs

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from data_structures import Event, InputData, Parameters, Seeker, Solution, Stats
from xlsx import FIRST_INDEX, OUTPUT_DIRECTORY_PATH, SheetNames, get_new_workbook

def save_to_xlsx(solution: Solution):
    xlsx = get_new_workbook()
    add_parameters(xlsx, solution.parameters)

    def add_participants():
        sheet = xlsx.create_sheet(SheetNames.PARTICIPANTS)
        _add_events_as_header(sheet, solution.events)
        _add_seekers_as_header(sheet, solution.seekers)
        for event, seekers in solution.participants.items():
            for seeker in seekers:
                index = solution.parameters.ordered_wishes[seeker].index(event)
                sheet[seeker.xlsx_column + event.xlsx_row] = index

    add_participants()

    makedirs(OUTPUT_DIRECTORY_PATH, exist_ok=True)
    xlsx.save(OUTPUT_DIRECTORY_PATH/f"{solution.stats.as_string}.xlsx")

def add_parameters(xlsx: Workbook, parameters: Parameters):
    add_input_data(xlsx, parameters.input_data)

    def add_rankings():
        sheet = xlsx.create_sheet(SheetNames.RANKINGS)
        _add_events_as_header(sheet, parameters.events)
        _add_seekers_as_header(sheet, parameters.seekers)
        for event, ranking in parameters.rankings.items():
            for seeker, rank in ranking.items():
                sheet[seeker.xlsx_column + event.xlsx_row] = rank

    add_rankings()

    def add_ordered_wishes():
        sheet = xlsx.create_sheet(SheetNames.ORDERED_WISHES)
        _add_events_as_header(sheet, parameters.events)
        _add_seekers_as_header(sheet, parameters.seekers)
        for seeker, events in parameters.ordered_wishes.items():
            for index, event in enumerate(events):
                sheet[seeker.xlsx_column + event.xlsx_row] = index

    add_ordered_wishes()

def add_input_data(xlsx: Workbook, input_data: InputData):
    add_stats(xlsx, input_data.stats)
    def add_events():
        sheet = xlsx.create_sheet(SheetNames.EVENTS)
        field_names = [field.name for field in fields(Event)]

        for column_index, field_name in enumerate(field_names, FIRST_INDEX):
            column = get_column_letter(column_index)
            sheet[column + "1"] = field_name
            for event in input_data.events:
                sheet[column + event.xlsx_row] = getattr(event, field_name)

    add_events()

    def add_seekers():
        sheet = xlsx.create_sheet(SheetNames.SEEKERS)
        field_names = [field.name for field in fields(Seeker)]

        for row_index, field_name in enumerate(field_names, FIRST_INDEX):
            row = str(row_index)
            sheet["A" + row] = field_name
            for seeker in input_data.seekers:
                sheet[seeker.xlsx_column + row] = getattr(seeker, field_name)

    add_seekers()

    def add_ranked_wishes():
        sheet = xlsx.create_sheet(SheetNames.RANKED_WISHES)
        _add_events_as_header(sheet, input_data.events)
        _add_seekers_as_header(sheet, input_data.seekers)
        for seeker, ranks in input_data.ranked_wishes.items():
            for rank, events in ranks.items():
                for event in events:
                    sheet[seeker.xlsx_column + event.xlsx_row] = rank

    add_ranked_wishes()

def add_stats(xlsx: Workbook, stats: Stats):
    sheet = xlsx.create_sheet(SheetNames.STATS)
    field_names = [field.name for field in fields(Stats)]

    for row_index, field_name in enumerate(field_names, FIRST_INDEX):
        row = str(row_index)
        sheet["A" + row] = field_name
        sheet["B" + row] = getattr(stats, field_name)


def _add_events_as_header(sheet: Worksheet, events: Iterable[Event]):
    for event in events:
        sheet["A" + event.xlsx_row] = event.as_string

def _add_seekers_as_header(sheet: Worksheet, seekers: Iterable[Seeker]):
    for seeker in seekers:
        sheet[seeker.xlsx_column + "1"] = seeker.as_string
