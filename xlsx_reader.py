from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook

from data_structures import Event, InputData, Parameters, Seeker, Solution, Stats
from hacks import FrozenDict, freeze_dict
from xlsx import SheetNames

def read_xlsx(xlsx_path: Path) -> Solution | Parameters | InputData | Stats | None:
    xlsx = load_workbook(xlsx_path)
    if SheetNames.STATS not in xlsx:
        return None
    
    stats = read_stats_from_xlsx(xlsx)

    if (SheetNames.EVENTS not in xlsx or
        SheetNames.SEEKERS not in xlsx or
        SheetNames.RANKED_WISHES not in xlsx):
        return stats
    
    input_data = read_input_data_from_xlsx(xlsx, stats)

    if (SheetNames.RANKINGS not in xlsx or
        SheetNames.ORDERED_WISHES not in xlsx):
        return input_data

    parameters = read_parameters_from_xlsx(xlsx, input_data)

    if SheetNames.PARTICIPANTS not in xlsx:
        return parameters
    
    return read_solution_from_xlsx(xlsx, parameters)


def read_solution_from_xlsx(xlsx: Workbook, parameters: Parameters) -> Solution:
    def get_participants() -> FrozenDict[Event, tuple[Seeker, ...]]:
        sheet = xlsx[SheetNames.PARTICIPANTS]
        participants: dict[Event, tuple[Seeker, ...]] = defaultdict(tuple)
        for event in parameters.events:
            for seeker in parameters.seekers:
                value = sheet[seeker.xlsx_column + event.xlsx_row].value
                if not value is None:
                    participants[event] += tuple([seeker])
        return freeze_dict(participants)
    
    participants = get_participants()

    return Solution(
        parameters=parameters,
        participants=participants
    )

def read_parameters_from_xlsx(xlsx: Workbook, input_data: InputData) -> Parameters:
    def get_rankings() -> FrozenDict[Event, FrozenDict[Seeker, int]]:
        sheet = xlsx[SheetNames.RANKINGS]
        rankings: dict[Event, FrozenDict[Seeker, int]] = dict()
        for event in input_data.events:
            ranking: dict[Seeker, int] = dict()
            for seeker in input_data.seekers:
                ranking[seeker] = sheet[seeker.xlsx_column + event.xlsx_row].value
            rankings[event] = freeze_dict(ranking)
        return freeze_dict(rankings)

    rankings = get_rankings()

    def get_ordered_wishes() -> FrozenDict[Seeker, tuple[Event, ...]]:
        sheet = xlsx[SheetNames.ORDERED_WISHES]
        ordered_wishes: dict[Seeker, tuple[Event, ...]] = dict()
        for seeker in input_data.seekers:
            ordered_wishes_as_dict: dict[Event, int] = dict()
            for event in input_data.events:
                index = sheet[seeker.xlsx_column + event.xlsx_row].value
                if not index is None:
                    ordered_wishes_as_dict[event] = index
            ordered_wishes[seeker] = tuple(sorted(
                ordered_wishes_as_dict.keys(),
                key=lambda event: ordered_wishes_as_dict[event]
            ))
        return freeze_dict(ordered_wishes)

    ordered_wishes = get_ordered_wishes()

    return Parameters(
        input_data=input_data,
        rankings=rankings,
        ordered_wishes=ordered_wishes
    )

def read_input_data_from_xlsx(xlsx: Workbook, stats: Stats) -> InputData:
    def read_events():
        sheet = xlsx[SheetNames.EVENTS]
        rows = sheet.iter_rows(values_only=True)
        field_names = [str(field_name) for field_name in next(rows)]
        events_as_dicts: list[dict[str, Any]] = list()
        for row in rows:
            events_as_dicts.append(_get_as_dict(row, field_names))
        return tuple([Event(**d) for d in events_as_dicts])
    
    events = read_events()

    def read_seekers():
        sheet = xlsx[SheetNames.SEEKERS]
        columns = sheet.iter_cols(values_only=True)
        field_names = [str(field_name) for field_name in next(columns)]
        seekers_as_dicts: list[dict[str, Any]] = list()
        for column in columns:
            seekers_as_dicts.append(_get_as_dict(column, field_names))
        return tuple(Seeker(**d) for d in seekers_as_dicts)

    seekers = read_seekers()

    def read_ranked_wishes() -> FrozenDict[Seeker, FrozenDict[int, tuple[Event, ...]]]:
        sheet = xlsx[SheetNames.RANKED_WISHES]
        ranked_wishes: dict[Seeker, FrozenDict[int, tuple[Event, ...]]] = dict()
        for seeker in seekers:
            wishes: dict[int, tuple[Event, ...]] = defaultdict(tuple)
            for event in events:
                rank = sheet[seeker.xlsx_column + event.xlsx_row].value
                if not rank is None:
                    wishes[rank] += tuple([event])
            ranked_wishes[seeker] = freeze_dict(wishes)
        return freeze_dict(ranked_wishes)

    ranked_wishes = read_ranked_wishes()

    return InputData(
        stats=stats,
        events=events,
        seekers=seekers,
        ranked_wishes=ranked_wishes
    )


def read_stats_from_xlsx(xlsx: Workbook) -> Stats:
    sheet = xlsx[SheetNames.STATS]
    columns = sheet.iter_cols(values_only=True)
    field_names = [str(field_name) for field_name in next(columns)]
    stats_as_dict = _get_as_dict(next(columns), field_names)
    return Stats(**stats_as_dict)


def _get_as_dict(cells: tuple[Any, ...], field_names: Iterable[str]) -> dict[str, Any]:
    return {field_name: cells[index] for index, field_name in enumerate(field_names)}