from dataclasses import dataclass
from random import shuffle

@dataclass
class JuLei:
    from_bw: bool
    wishes: list[int]

@dataclass
class Schulung:
    capacity: int
    juleis_hierarchy: list[JuLei]
    participants: list[JuLei]

    def update_participants(self, julei: JuLei) -> JuLei | None:
        self.participants.append(julei)
        if len(self.participants) <= self.capacity:
            return None
        return self._pop_least_fitting_julei()

    def _pop_least_fitting_julei(self) -> JuLei:
        least_fitting_julei = self.participants[0]
        for julei in self.participants:
            if self.juleis_hierarchy.index(julei) < self.juleis_hierarchy.index(least_fitting_julei):
                least_fitting_julei = julei
        self.participants.remove(least_fitting_julei)
        return least_fitting_julei

@dataclass
class Problem:
    name: str
    juleis: list[JuLei]
    schulungen: list[Schulung]
    def julei_is_allocated(self, julei: JuLei) -> bool:
        for schulung in self.schulungen:
            for allocated_julei in schulung.participants:
                if julei == allocated_julei:
                    return True
        return False

    def __init__(self, name: str, juleis: list[JuLei], capacities_per_schulung: list[int]) -> None:
        self.name = name
        self.juleis = juleis
        self.schulungen = list()
        for capacity in capacities_per_schulung:
            all_juleis_in_random_order = self.juleis[:]
            shuffle(all_juleis_in_random_order)
            self.schulungen.append(Schulung(max(1, capacity), all_juleis_in_random_order, list()))
