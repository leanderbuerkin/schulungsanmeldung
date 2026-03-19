from random import randint, shuffle

from data import Data, JuLei, Schulung

def get_random_data(
        number_of_schulungen: int,
        number_of_juleis: int,
        schulungen_capacity_range: tuple[int, int] = (6, 14),
        juleis_from_bw_in_percent: int = 80,
        range_of_number_of_wishes: tuple[int, int] = (1, 20),
    ):
    number_of_juleis_from_bw = number_of_juleis*(juleis_from_bw_in_percent/100)
    number_of_juleis_not_from_bw = number_of_juleis - number_of_juleis_from_bw
    
    name = f"{number_of_schulungen}_Schulungen_{number_of_juleis}_JuLeis"

    juleis: set[JuLei] = set()
    schulungen_indices = list(range(number_of_schulungen))
    for julei_index in range(number_of_juleis):
        shuffle(schulungen_indices)
        juleis.add(JuLei(
            julei_index,
            from_bw = julei_index > number_of_juleis_not_from_bw,
            wishes = tuple(schulungen_indices[:max(0, randint(*range_of_number_of_wishes))]),
        ))

    schulungen: set[Schulung] = set()
    for schulungs_index in range(number_of_schulungen):
        schulungen.add(Schulung(
            schulungs_index,
            capacity = max(1, randint(*schulungen_capacity_range)),
        ))

    return Data(name, juleis, schulungen)
