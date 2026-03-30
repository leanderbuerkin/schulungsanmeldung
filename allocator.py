from collections.abc import Iterable

from data_structures import Seeker, Solution, State, InputData, Event

from hacks import FrozenDict, freeze_dict
from allocation_logger import Logger


def find_best_allocation(parameters: InputData, processes_count_max: int = 1000) -> Solution:
    logger = Logger(parameters, processes_count_max)
    initial_state = State(wishes=parameters.flattened_wishes)
    final_state = _allocate(logger, parameters, initial_state)
    best_solution = Solution(
        index=0,
        parameters=parameters,
        initial_state=initial_state,
        final_state=final_state
    )

    # already called _get_solution() once, so start at 1
    for generated_solutions_count in range(1, processes_count_max):
        better_sorted_wishes = _get_sorted_wishes(parameters.seekers, best_solution.unsatisfied_demand)
        initial_state = State(wishes=better_sorted_wishes)
        final_state = _allocate(logger, parameters, initial_state)
        new_solution = Solution(
            index=generated_solutions_count,
            parameters=parameters,
            initial_state=initial_state,
            final_state=final_state
        )

        if new_solution.score > best_solution.score:
            logger.log_solution_update(best_solution, new_solution)
            best_solution = new_solution
        elif new_solution == best_solution:
            logger.log_final_solution(best_solution)
            break

    return best_solution

def _allocate(logger: Logger, parameters: InputData, initial_state: State) -> State:
    state = initial_state

    states_count = 1
    while len(state.overcrowded_events) > 0:
        state = _draw_candidates_once(parameters, state)
        states_count += 1
        logger.log_state_update(states_count, state)

    return state

def _draw_candidates_once(parameters: InputData, state: State) -> State:
    wishes = dict(state.wishes)

    for event, candidates in state.overcrowded_events.items():
        ranking = parameters.random_ranking[event]
        candidates = _sort_candidates(ranking, candidates)
        for candidate in candidates[event.capacity:]:
            wishes[candidate] = tuple(wishes[candidate][1:])

    return State(wishes=freeze_dict(wishes))

def _sort_candidates(
        random_ranking: FrozenDict[Seeker, int],
        unsorted_candidates: tuple[Seeker, ...]
    ) -> tuple[Seeker, ...]:
    """
    The best fitting candidate is at index 0.
    -> The lower the index, the better does the candidate fit.
    """
    candidates = list(unsorted_candidates)
    # Here you can add other properties of seekers that you want to sort for.
    # E.g. a gender/club quota or seekers with special needs like childcare or wheelchair-friendly.
    # The most important sort should be last.
    # The first property only decides the order of the events
    # which share the same value for all following properties.
    candidates.sort(key=lambda candidate: -random_ranking[candidate])  # first property (less important)
    candidates.sort(key=lambda candidate: not candidate.from_bw)  # second property (more important)

    return tuple(candidates)

def _get_sorted_wishes(seekers: Iterable[Seeker], demand: FrozenDict[Event, int]) -> FrozenDict[Seeker, tuple[Event, ...]]:
    """
    The best wish is at index 0.
    -> The wishes should be checked from lowest to highest index.
    """
    return freeze_dict({seeker: _sort_wishes(seeker.wishes, demand) for seeker in seekers})

def _sort_wishes(unsorted_wishes: tuple[tuple[Event, ...], ...], demand: FrozenDict[Event, int]) -> tuple[Event, ...]:
    """
    The best wish is at index 0.
    -> The wishes should be checked from lowest to highest index.
    """
    sorted_wishes: list[Event] = list()

    for wishes_with_equal_priority in unsorted_wishes:
        wishes = list(wishes_with_equal_priority)
        # Here you can add other properties of events that you want to sort for.
        # E.g. an event that should only take place if it is really necessary.
        # The most important sort should be last.
        # The first property only decides the order of the events
        # which share the same value for all following properties.
        wishes.sort(key=lambda event: -event.capacity)  # first property (less important)
        wishes.sort(key=lambda event: demand[event])  # second property (more important)
        sorted_wishes += wishes

    return tuple(sorted_wishes)
