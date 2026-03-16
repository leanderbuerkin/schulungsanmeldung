
from typing import Literal

from config import NUMBER_OF_PRIORITY_LEVELS
from data_containers import PriorityLevelsOfOneJuLei, Problem

def clear_priorities_of_julei(p: Problem, julei_index: int) -> None:
    p.julei_priorities[julei_index] = [set() for _ in range(NUMBER_OF_PRIORITY_LEVELS)]

def flatten_priorities(priorities: list[PriorityLevelsOfOneJuLei], priority_level: int) -> list[int]:
    """No clue how it works but the types say it does."""
    # Alternative to check all priority levels:
    # return [v for j in priorities for s in j for v in s]
    return [v for j in priorities for v in j[priority_level]]

def get_schulung_index_sorted_by_least_interest(p: Problem, julei_priorities: PriorityLevelsOfOneJuLei, priority_level: int) -> list[int]:
    """
    Returns the schulung first which rejects the least amount of JuLeis,
    if all interested JuLeis would get assigned.
    """
    all_allocations = [v for v in p.julei_allocations if v is not None]
    all_priorities = flatten_priorities(p.julei_priorities, priority_level)
    all_potentially_needed_places = all_allocations + all_priorities
    return sorted((i for i in julei_priorities[priority_level]), key=lambda i: all_potentially_needed_places.count(i) - p.schulung_max_juleis[i])

def recursion(
        p: Problem,
        sorted_unallocated_juleis: list[tuple[int, PriorityLevelsOfOneJuLei]],
        priority_level: int
    ) -> set[int] | Literal[True]:
    julei_index, julei_priorities = sorted_unallocated_juleis.pop()
    clear_priorities_of_julei(p, julei_index)
    place_needed_in_schulungen: set[int] = set()
    for schulung_index in get_schulung_index_sorted_by_least_interest(p, julei_priorities, priority_level):
        if p.is_full(schulung_index):
            place_needed_in_schulungen.add(schulung_index)
        else:
            p.julei_allocations[julei_index] = schulung_index
            if len(sorted_unallocated_juleis) == 0:
                return True
            recursion_result = recursion(p, sorted_unallocated_juleis, priority_level)
            if recursion_result is True:
                return True
            else:
                p.julei_allocations[julei_index] = None
                if schulung_index not in recursion_result:
                    sorted_unallocated_juleis.append((julei_index, julei_priorities))
                    p.julei_priorities[julei_index] = julei_priorities
                    return recursion_result
    sorted_unallocated_juleis.append((julei_index, julei_priorities))
    p.julei_priorities[julei_index] = julei_priorities
    return place_needed_in_schulungen

def get_unallocated_julei(p: Problem, priority_level: int) -> list[tuple[int, PriorityLevelsOfOneJuLei]]:
    """
    Returns a list of tuples, each tuple contains the index of one JuLei and the priorities of this JuLei.
    The JuLeis are ordered from many prioritized Schulungen to few.
    This way the greedy algorithm can pop the juleis and first allocates the JuLeis with little options.
    Later it still has the JuLeis with many options.
    """
    unallocated_juleis: list[tuple[int, PriorityLevelsOfOneJuLei]] = list()
    for julei_index, julei_priorities in enumerate(p.julei_priorities):
        if p.julei_allocations[julei_index] is None:
            unallocated_juleis.append((julei_index, julei_priorities))
    unallocated_juleis = sorted(unallocated_juleis, key=lambda x: len(x[1][priority_level]), reverse=True)
    return unallocated_juleis

def allocate(p: Problem) -> Problem:
    priority_level = 0
    unallocated_juleis = get_unallocated_julei(p, priority_level)
    # try to fit all
    recursion(p, unallocated_juleis, priority_level)
    return p
