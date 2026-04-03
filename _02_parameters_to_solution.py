from logging import INFO, basicConfig, info
from os import makedirs
from pathlib import Path

from data_structures import Event, Parameters, Seeker, Solution
from hacks import freeze_dict

LOG_DIRECTORY = Path(f"logs")

def get_solution(parameters: Parameters) -> Solution:
    makedirs(LOG_DIRECTORY, exist_ok=True)
    log_file_path = LOG_DIRECTORY / f"{parameters.name}.log"
    with open(log_file_path, "w"):  # deletes file content
        pass

    basicConfig(
        level=INFO,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=log_file_path
    )

    unchecked_wishes = {
        seeker: list(events)
        for seeker, events in parameters.ordered_wishes.items()
    }

    reallocated_seekers_count = 0
    participations: dict[Event, list[Seeker]] = {e: list() for e in parameters.events}
    for seeker, events in unchecked_wishes.items():
        if len(events) > 0:
            event = unchecked_wishes[seeker].pop(0)
            participations[event].append(seeker)
            reallocated_seekers_count += 1

    info(f'{10*'-'} Started Allocation "{parameters.name}" {10*'-'}')

    while reallocated_seekers_count > 0:
        rejected_seekers_count = 0
        reallocated_seekers_count = 0
        for event, candidates in participations.items():
            if len(candidates) <= event.capacity:
                continue
            ranking = parameters.rankings[event]
            candidates.sort(key=lambda seeker: ranking[seeker])

            participations[event] = candidates[:event.capacity]
    
            for rejected_seeker in candidates[event.capacity:]:
                wishes = unchecked_wishes[rejected_seeker]
                if len(wishes) > 0:
                    event = wishes.pop(0)
                    participations[event].append(rejected_seeker)
                    reallocated_seekers_count += 1
                else:
                    rejected_seekers_count += 1
        info(
            f"In this step, {reallocated_seekers_count} wishes got denied. "
            f"For {rejected_seekers_count} seekers it was their last wish."
        )

    info(f'{10*'-'} Finished Allocation "{parameters.name}" {10*'-'}')

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
