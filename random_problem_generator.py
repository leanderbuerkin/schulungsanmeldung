from random import randint, shuffle

from data_containers import JuLei, Problem

def generate_random_problem(
        number_of_schulungen: int,
        number_of_juleis: int,
        capacity_range: tuple[int, int] = (6, 14),
        juleis_from_bw_in_percent: int = 80,
        range_of_number_of_wishes: tuple[int, int] = (1, 20),
    ) -> Problem:
    name = f"{number_of_schulungen}_Schulungen_{number_of_juleis}_JuLeis"

    schulungen_indices = list(range(number_of_schulungen))
    number_of_juleis_from_bw = number_of_juleis*(juleis_from_bw_in_percent/100)
    juleis: list[JuLei] = list()
    for julei_index in range(number_of_juleis):
        shuffle(schulungen_indices)
        juleis.append(JuLei(
            from_bw = julei_index < number_of_juleis_from_bw,
            wishes = schulungen_indices[:max(0, randint(*range_of_number_of_wishes))],
        ))

    capacities_per_schulung = [randint(*capacity_range) for _ in range(number_of_schulungen)]

    return Problem(name, juleis, capacities_per_schulung)
