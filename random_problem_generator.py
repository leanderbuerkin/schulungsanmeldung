
from pathlib import Path

from data_containers import JuLei, JuLeiId, Problem, Schulung, SchulungsId
from file_saver import save_to_new_xlsx
from random import randint, shuffle

def generate_random_problem(
        output_directory: Path,
        number_of_schulungen: int,
        number_of_juleis: int,
        schulungen_capacity_range: tuple[int, int] = (6, 14),
        juleis_from_bw_in_percent: int = 80,
        range_of_number_of_wishes: tuple[int, int] = (1, 20),
    ):
    number_of_juleis_from_bw = number_of_juleis*(juleis_from_bw_in_percent/100)
    number_of_juleis_not_from_bw = number_of_juleis - number_of_juleis_from_bw


    juleis: dict[JuLeiId, JuLei] = dict()
    schulungen_indices = list(range(number_of_schulungen))
    for julei_index in range(number_of_juleis):
        shuffle(schulungen_indices)
        juleis[julei_index] = JuLei(
            julei_index,
            from_bw = julei_index > number_of_juleis_not_from_bw,
            wishes = schulungen_indices[:max(0, randint(*range_of_number_of_wishes))],
        )

    schulungen: dict[SchulungsId, Schulung] = dict()
    unique_scores = list(range(number_of_juleis))
    for schulungs_index in range(number_of_schulungen):
        shuffle(unique_scores)
        schulungen[schulungs_index] = Schulung(
            schulungs_index,
            capacity = max(1, randint(*schulungen_capacity_range)),
            scores={id: score for id, score in zip(juleis.keys(), unique_scores)}
        )

    p = Problem(
        f"{number_of_schulungen}_Schulungen_{number_of_juleis}_JuLeis",
        output_directory,
        juleis,
        schulungen,
        {id: list() for id in schulungen.keys()},
        {j.id: j.wishes for j in juleis.values()}
    )

    save_to_new_xlsx(p)
    return p
