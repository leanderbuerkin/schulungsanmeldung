"""
The data-structures are all immutable to make it easier to understand
and prevent errors like accidentally getting a reference instead of a copy.
"""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from hacks import FrozenDict, freeze_dict

# Different types to find misusage trough type errors.
type EventID = int
type SeekerID = str


@dataclass(frozen=True, slots=True, kw_only=True)
class Event:
    """Schulung"""
    id: EventID  # to be guaranteed unique
    capacity: int


@dataclass(frozen=True, slots=True, kw_only=True)
class Seeker:  # Applicant or Candidate is to long, so they are called Seeker
    """JuLei"""
    id: SeekerID  # to be guaranteed unique
    from_bw: bool  # bw=Baden-Württemberg
    wishes: tuple[tuple[Event, ...], ...]
    @property
    def flattened_wishes(self) -> tuple[Event, ...]:
        flattened_wishes: list[Event] = list()
        for wishes_with_equal_priority in self.wishes:
            flattened_wishes += wishes_with_equal_priority
        return tuple(flattened_wishes)


@dataclass(frozen=True, slots=True, kw_only=True)
class InputData:
    name: str
    events: tuple[Event, ...]
    seekers: tuple[Seeker, ...]
    random_ranking: FrozenDict[Event, FrozenDict[Seeker, int]]  # tie-breaker
    @property
    def flattened_wishes(self) -> FrozenDict[Seeker, tuple[Event, ...]]:
        return freeze_dict({seeker: seeker.flattened_wishes for seeker in self.seekers})
    @property
    def capacity_sum(self) -> int:
        return sum(event.capacity for event in self.events)
    @property
    def wishes_count(self) -> int:
        return sum(len(wishes) for wishes in self.flattened_wishes.values())
    @property
    def log_file_path(self) -> Path:
        return Path(f"{self.name}.log")

@dataclass(frozen=True, slots=True, kw_only=True)
class State:
    wishes: FrozenDict[Seeker, tuple[Event, ...]]
    @property
    def unallocatable_seekers(self) -> tuple[Seeker, ...]:
        return tuple(seeker for seeker, wishes in self.wishes.items() if len(wishes) == 0)
    @property
    def allocations(self) -> FrozenDict[Seeker, Event]:
        return freeze_dict({seeker: wishes[0] for seeker, wishes in self.wishes.items() if len(wishes) > 0})
    @property
    def candidates(self) -> FrozenDict[Event, tuple[Seeker, ...]]:
        candidates: dict[Event, list[Seeker]] = defaultdict(list)

        for seeker, event in self.allocations.items():
            candidates[event].append(seeker)

        return freeze_dict({event: tuple(seekers) for event, seekers in candidates.items()})
    @property
    def overcrowded_events(self) -> FrozenDict[Event, tuple[Seeker, ...]]:
        overcrowded_events: dict[Event, tuple[Seeker, ...]] = defaultdict(tuple)

        for event, candidates in self.candidates.items():
            if len(candidates) > event.capacity:
                overcrowded_events[event] = candidates

        return freeze_dict(overcrowded_events)

@dataclass(frozen=True, slots=True, kw_only=True)
class Solution:
    index: int
    parameters: InputData
    initial_state: State
    final_state: State
    @property
    def name(self) -> str:
        return f"Solution {self.index} for {self.parameters.name}"
    @property
    def participations(self) -> FrozenDict[Seeker, Event]:
        return self.final_state.allocations
    @property
    def participants(self) -> FrozenDict[Event, tuple[Seeker, ...]]:
        return self.final_state.candidates
    @property
    def unallocatable_seekers(self) -> tuple[Seeker, ...]:
        return self.final_state.unallocatable_seekers
    @property
    def unsatisfied_demand(self) -> FrozenDict[Event, int]:
        wishes_counts: dict[Event, int] = defaultdict(int)

        for seeker in self.unallocatable_seekers:
            for event in seeker.flattened_wishes:
                wishes_counts[event] += 1

        return freeze_dict(wishes_counts)
    @property
    def score(self) -> int:
        return len(self.participations)

    @property
    def total_wishes(self) -> FrozenDict[Seeker, tuple[Event, ...]]:
        return self.initial_state.wishes
    @property
    def accepted_wishes(self) -> FrozenDict[Seeker, tuple[Event]]:
        return freeze_dict({s: (e,) for s, e in self.final_state.allocations.items()})
    @property
    def unchecked_wishes(self) -> FrozenDict[Seeker, tuple[Event, ...]]:
        return freeze_dict({s: tuple(es[1:]) for s, es in self.final_state.wishes.items()})

    @property
    def total_wishes_count(self) -> int:
        return self.parameters.wishes_count
    @property
    def unchecked_wishes_count(self) -> int:
        return sum(len(wishes) for wishes in self.unchecked_wishes.values())
    @property
    def capacity_sum(self) -> int:
        return self.parameters.capacity_sum