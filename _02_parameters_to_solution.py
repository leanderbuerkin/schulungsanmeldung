from data_structures import Event, Parameters, Seeker, Solution
from hacks import freeze_dict

def get_solution(parameters: Parameters) -> Solution:
    unchecked_wishes = {
        seeker: list(events)
        for seeker, events in parameters.ordered_wishes.items()
    }

    participations: dict[Event, list[Seeker]] = {e: list() for e in parameters.events}

    unallocated_seekers: list[Seeker] = list(unchecked_wishes.keys())

    while len(unallocated_seekers) > 0:
        for seeker in unallocated_seekers:
            if len(unchecked_wishes[seeker]) == 0:
                continue
            event = unchecked_wishes[seeker].pop(0)
            participations[event].append(seeker)

        event, candidates = max(
            ((event, candidates) for event, candidates in participations.items()),
            key=lambda item: len(item[1]) - item[0].capacity
        )

        ranking = parameters.rankings[event]
        candidates.sort(key=lambda seeker: ranking[seeker])
        participations[event] = candidates[:event.capacity]
        unallocated_seekers = candidates[event.capacity:]

    participants: dict[Event, tuple[Seeker, ...]] = dict()
    for event in parameters.events:
        if event in participations:
            participants[event] = tuple(participations[event])
        else:
            participants[event] = tuple()

    return Solution(
        parameters=parameters,
        participants=freeze_dict(participants)
    )
