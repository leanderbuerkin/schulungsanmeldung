from collections import defaultdict
from random import shuffle

from data_structures import Event, InputData, Parameters, Seeker, Solution
from hacks import FrozenDict, freeze_dict


def choose_parameters(input_data: InputData, previous_solution: Solution | None) -> Parameters:
    def get_index() -> int:
        if previous_solution:
            return previous_solution.index + 1
        else:
            return 0

    def get_ordered_wishes():
        """
        The best wish is at index 0.
        -> The wishes should be checked from lowest to highest index.
    
        In this function you can add other properties of events that you want to sort for.
        E.g. an event that should only take place if it is really necessary.
        The most important sort should be last.
        The first property only decides the order of two events
        if they share the same value for all following properties.
        """
        if previous_solution:
            demand = previous_solution.unsatisfied_demand
        else:
            demand: FrozenDict[Event, int] = freeze_dict(defaultdict(int))
        ordered_wishes_per_seeker: dict[Seeker, tuple[Event, ...]] = defaultdict(tuple)
    
        for seeker, ranked_wishes in input_data.ranked_wishes.items():
            for rank in sorted(ranked_wishes.keys()):
                events = list(ranked_wishes[rank])
                events.sort(key=lambda event: -event.capacity) # first property (less important)
                events.sort(key=lambda event: demand[event])  # second property (more important)
                ordered_wishes_per_seeker[seeker] += tuple(events)
    
        return freeze_dict(ordered_wishes_per_seeker)

    def get_partially_random_rankings():
        """
        The best fitting candidate is at index 0.
        -> The lower the index, the better does the candidate fit.
    
        In this function you can add other properties of seekers that you want to sort for.
        E.g. a gender/club quota or seekers with special needs like childcare or wheelchair-friendly.
        The most important sort should be last.
        The first property only decides the order of two seekers
        if they share the same value for all following properties.
        """
        rankings: dict[Event, FrozenDict[Seeker, int]] = dict()
    
        for event in input_data.events:
            ranking = list(input_data.seekers)
            shuffle(ranking)
            ranking.sort(key=lambda seeker: not seeker.from_baden_wuerttemberg)
            rankings[event] = freeze_dict({seeker: rank for rank, seeker in enumerate(ranking)})

        return freeze_dict(rankings)

    return Parameters(
        input_data=input_data,
        index=get_index(),
        ordered_wishes=get_ordered_wishes(),
        rankings=get_partially_random_rankings()
    )
