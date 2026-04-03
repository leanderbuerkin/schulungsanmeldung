from random import choices, randint, shuffle

from data_structures import Event, InputData, Seeker, Stats
from hacks import FrozenDict, freeze_dict
import xlsx as XLSX


def generate_random_input_data(stats: Stats) -> InputData:
    def get_events() -> list[Event]:
        events: list[Event] = list()
    
        for row_index in XLSX.get_row_indizes(stats.events_count):
            events.append(Event(
                xlsx_row=row_index,
                capacity=_get_positive_randint(*stats.events_capacity_range)
            ))

        return events


    def get_seekers() -> list[Seeker]:
        seekers: list[Seeker] = list()

        for column_index in XLSX.get_column_indizes(stats.seekers_count):
            seekers.append(Seeker(
                xlsx_column=column_index,
                from_baden_wuerttemberg=randint(0,99) < stats.seekers_from_bw_in_percent
            ))

        return seekers


    def get_ranked_wishes(possible_wishes: list[Event]
                          ) ->  FrozenDict[int, tuple[Event, ...]]:
        wishes_count = _get_positive_randint(*stats.wishes_count_range)
        wishes = possible_wishes[:wishes_count]

        ranks_count = min(len(wishes), stats.wishes_ranks_count)
        cutting_indices = choices(range(len(wishes)), k=max(1, ranks_count))
        cutting_indices.sort()
        starts = [0] + cutting_indices
        stops = cutting_indices + [len(wishes)-1]
        slices = (slice(start, stop) for start, stop in zip(starts, stops))

        ranked_wishes_of_seeker: dict[int, tuple[Event, ...]] = dict()
        for rank, _slice in enumerate(slices):
            ranked_wishes_of_seeker[rank] = tuple(wishes[_slice])

        return freeze_dict(ranked_wishes_of_seeker)



    events = get_events()
    seekers = get_seekers()

    ranked_wishes: dict[Seeker, FrozenDict[int, tuple[Event, ...]]] = dict()
    for seeker in seekers:
        shuffle(events)
        ranked_wishes[seeker] = get_ranked_wishes(events)

    events.sort(key=lambda event: (len(event.xlsx_row), event.xlsx_row))
    seekers.sort(key=lambda seeker: (len(seeker.xlsx_column), seeker.xlsx_column))

    return InputData(
        stats=stats,
        events=tuple(events),
        seekers=tuple(seekers),
        ranked_wishes=freeze_dict(ranked_wishes)
    )

def _get_positive_randint(minimum: int, maximum: int) -> int:
    if minimum < 1:
        minimum = 1
    if maximum < minimum:
        maximum = minimum
    return randint(minimum, maximum)
