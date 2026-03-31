from collections import defaultdict

from data_structures import Event, Parameters, Seeker, Solution
from hacks import FrozenDict, freeze_dict
from allocation_logger import Logger


class Allocator:
    index: int
    parameters: Parameters
    prioritizations: dict[Seeker, tuple[Event, ...]]
    logger: Logger
    @property
    def name(self) -> str:
        return f"allocator_{self.index}_for_{self.parameters.name}"
    @property
    def _candidates(self) -> FrozenDict[Event, tuple[Seeker, ...]]:
        """
        The best fitting candidate is at index 0.
        -> The lower the index, the better does the candidate fit.
        """
        candidates: dict[Event, tuple[Seeker, ...]] = defaultdict(tuple)
        for seeker, events in self.prioritizations.items():
            if len(events) > 0:
                candidates[events[0]] += (seeker,)
        return freeze_dict(candidates)
    @property
    def _overcrowded_events(self) -> FrozenDict[Event, tuple[Seeker, ...]]:
        overcrowded_events: dict[Event, tuple[Seeker, ...]] = dict()
        for event, seekers in self._candidates.items():
            if len(seekers) > event.capacity:
                overcrowded_events[event] = seekers
        return freeze_dict(overcrowded_events)
    
    def __init__(self, parameters: Parameters, previous_solution: Solution | None = None, verbose_logging: bool = True):
        self.parameters = parameters
        self.logger = Logger(self, previous_solution, verbose_logging)

        if previous_solution is None:
            self.index = 0
            self.prioritizations = parameters.get_flattened_prioritizations()
        else:
            self.index = previous_solution.index + 1
            demand = previous_solution.unsatisfied_demand
            self.prioritizations = parameters.get_sorted_prioritizations(demand)

    def get_solution(self) -> Solution:
        while len(self._overcrowded_events) > 0:
            self.logger.log_update()
        
            for event, candidates in self._overcrowded_events.items():
                candidates = self.parameters.sort_candidates(candidates, event)
                for candidate in candidates[event.capacity:]:
                    self.prioritizations[candidate] = tuple(self.prioritizations[candidate][1:])

        solution = Solution(
            index=self.index,
            parameters=self.parameters,
            participants=self._candidates,
            participations=freeze_dict({seeker: events[0] for seeker, events in self.prioritizations.items()})
        )

        self.logger.log_final_solution(solution)
        return solution
