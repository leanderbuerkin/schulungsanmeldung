"""
The data-structures are all immutable to make it easier to understand
and prevent errors like accidentally getting a reference instead of a copy.
"""
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

from hacks import FrozenDict, freeze_dict


@dataclass(frozen=True, slots=True, kw_only=True)
class Event:
    xlsx_row: str
    capacity: int


@dataclass(frozen=True, slots=True, kw_only=True)
class Seeker:  # Applicants or Candidates is to long, so they are called Seekers
    xlsx_column: str
    from_baden_wuerttemberg: bool


@dataclass(frozen=True, slots=True, kw_only=True)
class Parameters:
    name: str
    prioritizations: FrozenDict[Seeker, tuple[tuple[Event, ...], ...]]
    random_orders: FrozenDict[Event, tuple[Seeker, ...]]
    solution_improvements_count_max: int

    @property  # not cached because we have no runtime constraint
    def seekers(self) -> tuple[Seeker, ...]:
        seekers = list(self.prioritizations.keys())
        seekers.sort(key=lambda seeker: (len(seeker.xlsx_column), seeker.xlsx_column))
        return tuple(seekers)
    @property  # not cached because we have no runtime constraint
    def events(self) -> tuple[Event, ...]:
        events = list(self.random_orders.keys())
        events.sort(key=lambda event: (len(event.xlsx_row), event.xlsx_row))
        return tuple(events)

    def get_flattened_prioritizations(self) -> dict[Seeker, tuple[Event, ...]]:
        return {seeker: self.get_flattened_prioritization(seeker) for seeker in self.seekers}

    def get_flattened_prioritization(self, seeker: Seeker) ->  tuple[Event, ...]:
        return sum(self.prioritizations[seeker], start=())

    def get_sorted_prioritizations(self, demand: FrozenDict[Event, int]) -> dict[Seeker, tuple[Event, ...]]:
        """
        The best wish is at index 0.
        -> The wishes should be checked from lowest to highest index.

        In this function you can add other properties of events that you want to sort for.
        E.g. an event that should only take place if it is really necessary.
        The most important sort should be last.
        The first property only decides the order of two events
        if they share the same value for all following properties.
        """
        sorted: dict[Seeker, tuple[Event, ...]] = defaultdict(tuple)

        for seeker, prioritization in self.prioritizations.items():
            for events_with_same_priority in prioritization:
                events = list(events_with_same_priority)
                events.sort(key=lambda event: -event.capacity)  # first property (less important)
                events.sort(key=lambda event: demand[event])  # second property (more important)
                sorted[seeker] += tuple(events)

        return sorted

    def sort_candidates(self, candidates: Iterable[Seeker], event: Event) -> tuple[Seeker, ...]:
        """
        The best fitting candidate is at index 0.
        -> The lower the index, the better does the candidate fit.

        In this function you can add other properties of seekers that you want to sort for.
        E.g. a gender/club quota or seekers with special needs like childcare or wheelchair-friendly.
        The most important sort should be last.
        The first property only decides the order of two seekers
        if they share the same value for all following properties.
        """
        random_order = self.random_orders[event]
        seekers = list(candidates)

        seekers.sort(key=lambda seeker: random_order.index(seeker))  # first property (less important)
        seekers.sort(key=lambda seeker: not seeker.from_baden_wuerttemberg)  # second property (more important)

        return tuple(seekers)


@dataclass(frozen=True, slots=True, kw_only=True)
class Solution:
    index: int
    parameters: Parameters
    participants: FrozenDict[Event, tuple[Seeker, ...]]
    participations: FrozenDict[Seeker, Event | None]
    @property
    def name(self) -> str:
        return f"solution_{self.index}_for_{self.parameters.name}"
    @property
    def satisfied_seekers_count(self) -> int:
        return sum(not(event is None) for event in self.participations.values())
    @property
    def unsatisfied_demand(self) -> FrozenDict[Event, int]:
        demand: dict[Event, int] = defaultdict(int)
        for seeker, participation in self.participations.items():
            if participation is None:
                for event in self.parameters.get_flattened_prioritization(seeker):
                    demand[event] += 1
        return freeze_dict(demand)
