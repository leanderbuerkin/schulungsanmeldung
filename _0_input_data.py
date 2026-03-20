"""
These dataclasses are used as keys in dicts.

That's why they are frozen, get a unique id and are using tuples.
"""

from dataclasses import dataclass
from random import randint, shuffle

type UniqueSchulungsId = int    # just for readability
type UniqueJuLeiId = int    # just for readability

@dataclass(frozen=True)
class Schulung:
    id: UniqueSchulungsId
    capacity: int

@dataclass(frozen=True)
class JuLei:
    id: UniqueJuLeiId
    from_bw: bool
    # Tuple to make it hashable for the set.
    wishes: tuple[UniqueSchulungsId, ...]

@dataclass(frozen=True)
class InputData:
    name: str
    schulungen: set[Schulung]
    juleis: set[JuLei]

@dataclass(frozen=True)
class StatsForRandomData:
    number_of_schulungen: int
    number_of_juleis: int
    schulungen_capacity_range: tuple[int, int]
    range_of_number_of_wishes: tuple[int, int]
    juleis_from_bw_in_percent: int

def get_random_input_data(stats: StatsForRandomData) -> InputData:
    name = f"{stats.number_of_schulungen}_Schulungen_"
    name += f"{stats.number_of_juleis}_JuLeis"

    schulungen: set[Schulung] = set()
    for schulungs_index in range(stats.number_of_schulungen):
        schulungen.add(Schulung(
            schulungs_index,
            capacity = max(1, randint(*stats.schulungen_capacity_range)),
        ))

    juleis: set[JuLei] = set()
    schulungen_indices = [s.id for s in schulungen]
    for julei_index in range(stats.number_of_juleis):
        shuffle(schulungen_indices)
        number_of_wishes = max(0, randint(*stats.range_of_number_of_wishes))
        juleis.add(JuLei(
            julei_index,
            from_bw = randint(0, 99) < stats.juleis_from_bw_in_percent,
            # Tuple to make it hashable for the set.
            wishes = tuple(schulungen_indices[:number_of_wishes]),
        ))

    return InputData(name, schulungen, juleis)
