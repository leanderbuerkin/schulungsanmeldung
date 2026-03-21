from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property

from experimental_hack import Unpackable

type UniqueSchulungsId = int    # just for readability
type UniqueJuLeiId = int    # just for readability

@dataclass(frozen=True, slots=True, kw_only=True)
class SchulungFromOdoo(Unpackable):
    # Used as keys in dicts.
    # So each instance must be unique and immutable.
    id: UniqueSchulungsId
    capacity: int

@dataclass(frozen=True, slots=True, kw_only=True)
class JuLeiFromOdoo(Unpackable):
    # Used as keys in dicts.
    # So each instance must be unique and immutable.
    # Sets, lists and dicts are mutable, tuples are not.
    id: UniqueJuLeiId
    from_bw: bool
    # Tuple to make it hashable for the set.
    wishes: tuple[UniqueSchulungsId, ...]

@dataclass(frozen=True, slots=True, kw_only=True)
class InputData:
    name: str
    schulungen: set[SchulungFromOdoo]
    juleis: set[JuLeiFromOdoo]

@dataclass(frozen=True, slots=True, kw_only=True)
class JuLei(JuLeiFromOdoo):
    pass

@dataclass(frozen=True, slots=True, kw_only=True)
class Schulung(SchulungFromOdoo):
    """
    If two JuLeis compete for a slot in a Schulung
    the JuLei that comes first in the ranking, gets the slot.
    """
    ranking: tuple[UniqueJuLeiId, ...]

@dataclass(frozen=True, kw_only=True) # no slots to use cached_property
class CompleteData:
    """
    It is called "complete data" because the participants list
    can be generated from this and is always the same.

    To always have the same result,
    each schulung gets a random ranking of JuLeis.

    To always take the same steps to the result,
    the order of the Schulungen and JuLeis is fixed.

    Additionaly some quality of life methods are added.
    """
    name: str
    schulungen: tuple[Schulung, ...]
    juleis: tuple[JuLei, ...]

    @cached_property
    def schulungen_by_id(self) -> dict[UniqueSchulungsId, Schulung]:
        return {s.id: s for s in self.schulungen}
    @cached_property
    def juleis_by_id(self) -> dict[UniqueJuLeiId, JuLei]:
        return {j.id: j for j in self.juleis}
    @cached_property
    def wishes(self) -> dict[JuLei, list[Schulung]]:
        wishes_of_juleis: dict[JuLei, list[Schulung]] = defaultdict(list)
        for julei in self.juleis:
            for schulungs_id in julei.wishes:
                wish_of_julei = self.schulungen_by_id[schulungs_id]
                wishes_of_juleis[julei].append(wish_of_julei)
        return wishes_of_juleis
    @cached_property
    def number_of_wishes(self) -> int:
        return sum(len(ws) for ws in self.wishes.values())
    @cached_property
    def number_of_slots(self) -> int:
        return sum(s.capacity for s in self.schulungen)

@dataclass(frozen=True, slots=True, kw_only=True)
class ParticipantsList:
    """
    Which JuLei participates in which Schulung is stored in two ways:

    - Once the participants for each Schulung
    - Once the Schulung each JuLei participates in

    This way we do not loose the information which Schulung stays empty
    and which JuLei does not participate in any Schulung.
    """
    participants: dict[Schulung, list[JuLei]]
    participations: dict[JuLei, Schulung | None]

@dataclass(kw_only=True)
class State:
    parameters: CompleteData

    allocations: dict[Schulung, list[JuLei]]
    unchecked_wishes: dict[JuLei, list[Schulung]]
    overcrowded_schulungen: set[Schulung]
    time: float

    @property
    def searching_juleis(self) -> set[JuLei]:
        searching_juleis: set[JuLei] = set()
        for julei, wishes in self.unchecked_wishes.items():
            if not self.is_allocated(julei) and len(wishes) > 0:
                searching_juleis.add(julei)
        return searching_juleis

    def is_allocated(self, julei: JuLei) -> Schulung | None:
        for schulung, juleis in self.allocations.items():
            if julei in juleis:
                return schulung
        return None

    def can_not_be_allocated(self, julei: JuLei) -> bool:
        return julei not in self.searching_juleis and self.is_allocated(julei) is None

    def assign_juleis_ignoring_schulungs_capacity(self):
        unchecked_wishes = self.unchecked_wishes
        for julei in self.searching_juleis:
            desired_schulung = unchecked_wishes[julei].pop(0)
            self.add_allocation(desired_schulung, julei)

    def enforce_schulungs_capacity(self):
        while len(self.overcrowded_schulungen) > 0:
            schulung = next(iter(self.overcrowded_schulungen))

            # Lower properties are only considered, if the ones before are equal.
            self.allocations[schulung].sort(key=lambda julei:(
                julei.from_bw,
                schulung.ranking.index(julei.id)
            ))
            while schulung in self.overcrowded_schulungen:
                self.remove_one_julei(schulung)

    def add_allocation(self, schulung: Schulung, julei: JuLei):
        self.allocations[schulung].append(julei)
        if len(self.allocations[schulung]) > schulung.capacity:
            self.overcrowded_schulungen.add(schulung)

    def remove_one_julei(self, schulung: Schulung):
        self.allocations[schulung].pop(0)
        if len(self.allocations[schulung]) <= schulung.capacity:
            self.overcrowded_schulungen.remove(schulung)
