from collections.abc import Iterable
from openpyxl.utils import get_column_letter
from random import choices, randint, shuffle

from data_structures import InputData, Event, Seeker
from hacks import FrozenDict, freeze_dict

def generate_random_input_data(
        events_count: int,
        seekers_count: int,
        seekers_from_bw_in_percent: int,
        events_capacity_min: int,
        events_capacity_max: int,
        wishes_count_min: int,
        wishes_count_max: int,
        wishes_levels: int = 3
    ) -> InputData:

    events: set[Event] = set()
    for event_id in generate_unique_integers(events_count):
        events.add(Event(
            id = event_id,
            capacity = generate_random_positive_integer(events_capacity_min, events_capacity_max)
        ))

    seekers: set[Seeker] = set()
    for seeker_id in generate_unique_strings(seekers_count):
        seekers.add(Seeker(
            id = seeker_id,
            from_bw = randint(0, 99) < seekers_from_bw_in_percent,
            wishes = generate_random_wishes(wishes_count_min, wishes_count_max, wishes_levels, list(events))
        ))

    return InputData(
        name=f"{events_count}_Events_{seekers_count}_Seekers",
        events = tuple(sorted(events, key=lambda e: e.id)),
        seekers = tuple(sorted(seekers, key=lambda s: s.id)),
        random_ranking = generate_random_ranking(events, list(seekers))
    )

XLSX_FIRST_ID = 2  # XLSXstarts with 1 which is the header

def generate_unique_integers(amount: int) -> list[int]:
    """Returns XLSX row indizes."""
    return [i for i in range(XLSX_FIRST_ID, XLSX_FIRST_ID + amount)]

def generate_unique_strings(amount: int) -> list[str]:
    """Returns XLSX column indizes."""
    return [get_column_letter(i) for i in generate_unique_integers(amount)]

def generate_random_positive_integer(minimum: int, maximum: int) -> int:
    if minimum < 0:
        minimum = 0
    if maximum < minimum:
        maximum = minimum
    return randint(minimum, maximum)

def generate_random_wishes(
        minimum: int,
        maximum: int,
        levels_count: int,
        possible_wishes: list[Event]
    ) -> tuple[tuple[Event, ...], ...]:
    shuffle(possible_wishes)
    wishes = possible_wishes[:generate_random_positive_integer(minimum, maximum)]
    levels_count = min(levels_count, len(wishes))

    cutting_indices = sorted(choices(range(len(wishes)), k=levels_count))
    start_indices = [0] + cutting_indices
    stop_indices = cutting_indices + [len(wishes)-1]

    wishes_with_levels: list[tuple[Event, ...]] = list()
    for start, stop in zip(start_indices, stop_indices):
        wishes_with_levels.append(tuple(wishes[start:stop]))

    return tuple(wishes_with_levels)

def generate_random_ranking(
        events: Iterable[Event],
        seekers: list[Seeker]
    ) -> FrozenDict[Event, FrozenDict[Seeker, int]]:
    ranking: dict[Event, FrozenDict[Seeker, int]] = dict()

    for event in events:
        shuffle(seekers)
        ranking[event] = freeze_dict({seeker: rank for rank, seeker in enumerate(seekers)})

    return freeze_dict(ranking)
