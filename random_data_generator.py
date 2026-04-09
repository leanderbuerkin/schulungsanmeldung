from collections import defaultdict
from dataclasses import dataclass
from random import randint, shuffle

from allocator import Event, Seeker


@dataclass(frozen=True, slots=True, kw_only=True)
class Stats:
    events_count: int
    seekers_count: int
    seekers_from_bw_in_percent: int
    events_capacity_min: int
    events_capacity_max: int
    wishes_per_rank_min: int
    wishes_per_rank_max: int
    wishes_ranks_count: int


def generate_random_input_data(stats: Stats) -> dict[int, dict[Seeker, list[Event]]]:
    events = [
        Event(index=index, capacity=_get_random_capacity(stats))
        for index in range(stats.events_count)
    ]

    seekers = [
        Seeker(index=index, from_baden_wuerttemberg=randint(0,99) < stats.seekers_from_bw_in_percent)
        for index in range(stats.seekers_count)
    ]

    ranked_wishes: dict[int, dict[Seeker, list[Event]]] = defaultdict(dict)
    for seeker in seekers:
        for rank in range(stats.wishes_ranks_count):
            shuffle(events)
            wishes_count = _get_positive_randint(stats.wishes_per_rank_min, stats.wishes_per_rank_max)
            ranked_wishes[rank][seeker] = events[:wishes_count]

    return ranked_wishes

def _get_random_capacity(stats: Stats) -> int:
    return _get_positive_randint(stats.events_capacity_min, stats.events_capacity_max)

def _get_positive_randint(minimum: int, maximum: int) -> int:
    if minimum < 1:
        minimum = 1
    if maximum < minimum:
        maximum = minimum
    return randint(minimum, maximum)
