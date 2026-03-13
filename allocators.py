from dataclasses import dataclass
from math import nan
from collections.abc import Callable, Generator

from numpy import float64
from pandas import isna

from data_containers import JuLei, Problem, Schulung

@dataclass(frozen=True)
class ToYield:
    cleanup: bool
    allocations: bool
    failed_allocations: bool

def remove_negative_preferences(p: Problem) -> tuple[Problem, str]:
    p.preferences[p.preferences < 0] = nan
    return p, "removed_negative_values"

def scale_each_preference_column_to_one(p: Problem) -> tuple[Problem, str]:
    p.preferences = p.preferences / p.preferences.sum(axis=0)
    return p, "scaled_each_column_to_one"

def get_allocations_by_priorities(p: Problem,
        fulfills_requirements: Callable[[JuLei], bool]
    ) -> list[tuple[Schulung, JuLei, float64]]:
    """Can not be a generator, because it gets sorted."""
    allocations: list[tuple[Schulung, JuLei, float64]] = list()
    for schulung in p.schulungen:
        for julei in p.juleis:
            if not fulfills_requirements(julei):
                continue
            preference = p.get_preference(schulung, julei)
            if not isna(preference):
                allocations.append((schulung, julei, preference))
    allocations = sorted(allocations, key=lambda x: x[2], reverse=True)
    return allocations

def allocate_by_priority(p: Problem, to_yield: ToYield = ToYield(True, False, True)) -> Generator[tuple[Problem, str]]:
    p, message = remove_negative_preferences(p)
    p, message = scale_each_preference_column_to_one(p)
    if to_yield.cleanup:
        yield p, message

    allocations = get_allocations_by_priorities(p, lambda j: j.from_bawue)
    allocations += get_allocations_by_priorities(p, lambda j: not j.from_bawue)

    for schulung, julei, _ in allocations:
        if not p.get_allocation(julei) is None:
            continue
        if p.is_full(schulung):
            if to_yield.failed_allocations:
                yield p, f"{schulung.schulungsnummer}_is_full_and_rejected_{julei.name}"
        else:
            p.add_allocation(schulung, julei)
            if to_yield.allocations:
                yield p, f"allocated_{julei.name}_to_{schulung.schulungsnummer}"

def reallocate_to_fit_all_juleis(p: Problem, to_yield: ToYield = ToYield(True, False, True)) -> Generator[tuple[Problem, str]]:
    allocations_of_unassigned_juleis = get_allocations_by_priorities(p, lambda j: p.get_allocation(j) is None)
    for schulung, julei, _ in allocations_of_unassigned_juleis:
        if not p.get_allocation(julei) is None:
            continue
        reallocations = explore_reallocation(p, schulung, set())
        if reallocations is None:
            if to_yield.failed_allocations:
                yield p, f"{schulung.schulungsnummer}_is_full_and_rejected_{julei.name}"
        else:
            for reallocated_schulung, reallocated_julei in reversed(reallocations):
                p.remove_allocation(reallocated_julei)
                p.add_allocation(reallocated_schulung, reallocated_julei)
                if to_yield.allocations:
                    yield p, f"reallocated_{reallocated_julei.name}_to_{reallocated_schulung.schulungsnummer}"
            p.add_allocation(schulung, julei)
            if to_yield.allocations:
                yield p, f"allocated_{julei.name}_to_{schulung.schulungsnummer}"

def explore_reallocation(
        p: Problem,
        full_schulung: Schulung,
        visited_schulungen: set[Schulung]
    ) -> list[tuple[Schulung, JuLei]] | None:
    visited_schulungen = visited_schulungen | {full_schulung}
    reallocations = get_allocations_by_priorities(p, lambda j: p.get_allocation(j) is full_schulung)

    for schulung, julei,_ in reallocations:
        if schulung in visited_schulungen or p.is_full(schulung):
            continue
        else:
            return [(schulung, julei)]

    reallocations_all_schulungen_full = reallocations

    for schulung, julei,_ in reallocations_all_schulungen_full:
        if schulung in visited_schulungen:
            continue
        elif p.is_full(schulung):
            further_reallocations = explore_reallocation(p, schulung, visited_schulungen)
            if not further_reallocations is None:
                return [(schulung, julei)] + further_reallocations
