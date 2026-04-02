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
        if events
    }
    
    rankings: dict[Event, dict[Seeker, int]] = dict()
    for event, ranking in parameters.rankings.items():
        for seeker, rank in ranking.items():
            if seeker not in unchecked_wishes:
                continue
            if event not in unchecked_wishes[seeker]:
                continue
            if event not in rankings.keys():
                rankings[event] = dict()
            rankings[event][seeker] = rank


    info(f'{10*'-'} Started Allocation "{parameters.name}" {10*'-'}')

    while True:
        reallocated_seekers_count = 0
        denied_seekers_count = 0

        for event, ranking in rankings.items():

            candidates = (
                seeker for seeker in ranking.keys()
                if unchecked_wishes[seeker][0] == event
            )
            candidates = sorted(candidates, key=lambda seeker: ranking[seeker])

            for rejected_candidate in candidates[event.capacity:]:
                if len(unchecked_wishes[rejected_candidate]) == 1:
                    # Deleting all rejected seekers ensures that
                    # unchecked_wishes.pop(0) and unchecked_wishes[0] is always possible.
                    del unchecked_wishes[rejected_candidate]
                    del rankings[event][rejected_candidate]
                    denied_seekers_count += 1
                else:
                    unchecked_wishes[rejected_candidate].pop(0)
                    del rankings[event][rejected_candidate]
                    reallocated_seekers_count += 1

        denied_wishes = denied_seekers_count + reallocated_seekers_count
        info(
            f"In this step, {denied_wishes} wishes got denied. " +
            f"For {denied_seekers_count} seekers it was their last wish."
        )
        if reallocated_seekers_count == 0:
            break

    info(f'{10*'-'} Finished Allocation "{parameters.name}" {10*'-'}')

    participations: dict[Seeker, Event | None] = dict()
    for seeker in parameters.seekers:
        if seeker in unchecked_wishes.keys():
            participations[seeker] = unchecked_wishes[seeker][0]
        else:
            participations[seeker] = None

    return Solution(
        parameters=parameters,
        participations=freeze_dict(participations)
    )
