from dataclasses import replace
from pathlib import Path
from random import choices, randint, shuffle
from time import gmtime, strftime, time

from data_structures import InputData, SchulungFromOdoo, JuLeiFromOdoo
from data_structures import CompleteData, Schulung, JuLei
from data_structures import ParticipantsList, State
from xlsx import XLSXPlotter

def generate_random_input_data(
        number_of_schulungen: int,
        number_of_juleis: int,
        juleis_from_bw_in_percent: int,
        schulungen_capacity_min: int,
        schulungen_capacity_max: int,
        number_of_wishes_min: int,
        number_of_wishes_max: int,
    ) -> InputData:

    capacities = list(choices(
        _as_valid_range(schulungen_capacity_min, schulungen_capacity_max),
        k=number_of_schulungen
    ))
    schulungen_indices = list(range(number_of_schulungen))
    numbers_of_wishes = list(choices(
        _as_valid_range(number_of_wishes_min, number_of_wishes_max),
        k=number_of_juleis
    ))

    capacities.sort()  # optional
    numbers_of_wishes.sort()  # optional

    schulungen: set[SchulungFromOdoo] = set()
    for schulungs_index, capacity in enumerate(capacities):
        schulungen.add(SchulungFromOdoo(
            id = schulungs_index,
            capacity = capacity
        ))

    juleis: set[JuLeiFromOdoo] = set()
    for julei_index, number_of_wishes in enumerate(numbers_of_wishes):
        shuffle(schulungen_indices)
        juleis.add(JuLeiFromOdoo(
            id = julei_index,
            from_bw = randint(0, 99) < juleis_from_bw_in_percent,
            # Tuple to make it hashable.
            wishes = tuple(schulungen_indices[:number_of_wishes]),
        ))

    return InputData(
        name=f"{number_of_schulungen}_Schulungen_{number_of_juleis}_JuLeis",
        schulungen = schulungen,
        juleis = juleis
    )

def _as_valid_range(minimum: int, maximum: int) -> range:
    minimum = max(minimum, 0)
    maximum = max(maximum, minimum)
    return range(minimum, maximum + 1)

def complete_data(data: InputData) -> CompleteData:
        juleis: list[JuLei] = list()
        for julei in data.juleis:
            juleis.append(JuLei(
                **julei
            ))

        schulungen: list[Schulung] = list()
        for schulung in data.schulungen:
            shuffle(juleis)
            schulungen.append(Schulung(
                **schulung,
                ranking=tuple((j.id for j in juleis))
            ))

        schulungen.sort(key=lambda s: s.id)
        juleis.sort(key=lambda j: j.id)

        return CompleteData(
            name = data.name,
            schulungen = tuple(schulungen),
            juleis = tuple(juleis)
        )

def generate_participants_list(
        data: CompleteData,
        save_steps_to_xlsx: Path | None,
        max_number_of_plots: int | None = 30
    ) -> ParticipantsList | None:
    print("")
    states: list[State] = list()

    state = State(
        parameters=data,
        allocations={s: list() for s in data.schulungen},
        unchecked_wishes=data.wishes,
        overcrowded_schulungen=set(),
        time=time()
    )

    states.append(replace(state))

    while len(state.searching_juleis) > 0:
        state.assign_juleis_ignoring_schulungs_capacity()
        states.append(replace(state, time=time()))
        state.enforce_schulungs_capacity()
        states.append(replace(state, time=time()))
        _generate_console_output(states)

    participants_list = ParticipantsList(
        participants = state.allocations,
        participations = {j: state.is_allocated(j) for j in state.parameters.juleis}
    )

    if save_steps_to_xlsx:
        XLSXPlotter.save_to_xlsx(states[:max_number_of_plots], save_steps_to_xlsx)

    _generate_final_console_output(states)

    return participants_list

def _generate_console_output(states: list[State]):
    passed_time = states[-1].time - states[0].time
    remaining_steps_guess = max(len(ws) for ws in states[-1].unchecked_wishes.values())
    finished_steps = len(states) // 2  # 2 states per step

    total_steps_guess = finished_steps + remaining_steps_guess
    time_per_step = passed_time / max(1, finished_steps)
    remaining_time_guess = remaining_steps_guess * time_per_step
    progress_guess = (100*finished_steps) // max(1, total_steps_guess)

    print(
        f"{progress_guess:<1} % in "+
        f"{strftime("%H:%M:%S.%f"[:-3], gmtime(passed_time))} " +
        f"-> ETA: {strftime("%H:%M:%S", gmtime(remaining_time_guess))}",
        sep="\n"
    )

def _generate_final_console_output(states: list[State]):
    passed_time = states[-1].time - states[0].time
    steps = len(states) // 2  # 2 states per step
    data = states[-1].parameters
    number_of_wishes = sum((len(ws) for ws in data.wishes.values()))
    average_number_of_wishes = number_of_wishes//len(data.juleis)
    average_number_of_slots = data.number_of_slots//len(data.schulungen)
    number_of_allocated_juleis = len({j for j in data.juleis if states[-1].is_allocated(j)})

    print(
        f"",
        f"{22*"-"} Finished! {22*"-"}",
        f"",
        f"Allocated {len(data.juleis)} JuLeis with {number_of_wishes} wishes (~{average_number_of_wishes} per JuLei)",
        f"to {data.number_of_slots} Slots in {len(data.schulungen)} Schulungen (~{average_number_of_slots} per Schulung).",
        f"This took {steps} steps and {strftime("%H:%M:%S.%f"[:-3], gmtime(passed_time))}.",
        f"{number_of_allocated_juleis} JuLeis got a slot, " +
        f"{len(data.juleis) - number_of_allocated_juleis} did not.",
        f"",
        sep="\n"
    )
