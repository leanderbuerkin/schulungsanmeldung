from collections import defaultdict
from dataclasses import dataclass

from hacks import FrozenDict, freeze_dict

@dataclass(frozen=True, slots=True, kw_only=True)
class Event:
    xlsx_row: str # makes each instance unique
    capacity: int
    # Be aware when adding further attributes:
    # Lists, dicts, tuples and other types might cause problems.
    # E.g. JSON converts tuples to lists.


@dataclass(frozen=True, slots=True, kw_only=True)
class Seeker:
    xlsx_column: str # makes each instance unique
    from_baden_wuerttemberg: bool
    # Be aware when adding further attributes:
    # Lists, dicts, tuples and other types might cause problems.
    # E.g. JSON converts tuples to lists.


@dataclass(frozen=True, slots=True, kw_only=True)
class Stats:
    events_count: int
    seekers_count: int
    seekers_from_bw_in_percent: int
    events_capacity_range: tuple[int, int]
    wishes_count_range: tuple[int, int]
    wishes_ranks_count: int

    @property
    def as_string(self) -> str:
        name = f"{self.events_count}_events__"
        name += f"{self.seekers_count}_seekers__"
        name += f"{self.events_capacity_range[0]}_to_"
        name += f"{self.events_capacity_range[1]}_slots__"
        name += f"{self.wishes_count_range[0]}_to_"
        name += f"{self.wishes_count_range[1]}_wishes__"
        name += f"{self.wishes_ranks_count}_ranks"
        name.replace("-", "_minus_")
        return name


@dataclass(frozen=True, slots=True, kw_only=True)
class InputData:
    name: str
    events: tuple[Event, ...]
    seekers: tuple[Seeker, ...]
    ranked_wishes: FrozenDict[Seeker, FrozenDict[int, tuple[Event, ...]]]


@dataclass(frozen=True, slots=True, kw_only=True)
class Parameters:
    input_data: InputData
    index: int
    rankings: FrozenDict[Event, FrozenDict[Seeker, int]]
    ordered_wishes: FrozenDict[Seeker, tuple[Event, ...]]
    @property
    def name(self) -> str:
        return f"{self.input_data.name}__{self.index:03d}"
    @property
    def events(self) -> tuple[Event, ...]:
        return self.input_data.events
    @property
    def seekers(self) -> tuple[Seeker, ...]:
        return self.input_data.seekers


@dataclass(frozen=True, slots=True, kw_only=True)
class Solution:
    parameters: Parameters
    participants: FrozenDict[Event, tuple[Seeker, ...]]
    @property
    def index(self) -> int:
        return self.parameters.index
    @property
    def name(self) -> str:
        return f"solution_{self.index}_for_{self.parameters.input_data.name}"
    @property
    def events(self) -> tuple[Event, ...]:
        return self.parameters.events
    @property
    def seekers(self) -> tuple[Seeker, ...]:
        return self.parameters.seekers
    @property
    def participations(self) -> FrozenDict[Seeker, Event | None]:
        participations: dict[Seeker, Event | None] = {s: None for s in self.seekers}
        for event, seekers in self.participants.items():
            for seeker in seekers:
                participations[seeker] = event
        return freeze_dict(participations)
    @property
    def satisfied_seekers(self) -> tuple[Seeker, ...]:
        return tuple(seeker for seeker, event in self.participations.items() if event)
    @property
    def unsatisfied_seekers(self) -> tuple[Seeker, ...]:
        return tuple(seeker for seeker, event in self.participations.items() if event is None)
    @property
    def unsatisfied_demand(self) -> FrozenDict[Event, int]:
        demand: dict[Event, int] = defaultdict(int)
        for seeker in self.unsatisfied_seekers:
            for event in self.parameters.ordered_wishes[seeker]:
                demand[event]
        return freeze_dict(demand)
