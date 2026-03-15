from dataclasses import dataclass

# Contains as many sets as defined in config.py
type PriorityLevelsOfOneJuLei = list[set[int]]

@dataclass
class Problem:
    schulung_max_juleis: list[int]
    julei_from_bw: list[bool]
    julei_priorities: list[PriorityLevelsOfOneJuLei]
    julei_allocations: list[int | None]

    def is_full(self, schulung_index: int) -> bool:
        return self.julei_allocations.count(schulung_index) >= self.schulung_max_juleis[schulung_index]
