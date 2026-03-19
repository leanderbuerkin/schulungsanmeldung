"""
The JuLeis and Schulungen are stored as a list to ensure that
for the same input the processes are executed in the same order.

The keys in the dictionary can be in different order
the result should always be the same,
but the steps to reach it might differ.
"""
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from random import shuffle

from input_data import JuLei, Schulung, UniqueJuLeiId, UniqueSchulungsId

@dataclass
class Data:
    """
    If two JuLeis compete for a slot of a Schulung,
    the JuLei with the higher score for this Schulung gets the slot.
    """
    name: str
    juleis: list[JuLei]
    schulungen: list[Schulung]
    juleis_by_id: dict[UniqueJuLeiId, JuLei]
    schulungen_by_id: dict[UniqueSchulungsId, Schulung]
    scores: dict[Schulung, dict[JuLei, int]]

    @property
    def total_capacity(self) -> int:  # for time estimates
        return sum((s.capacity for s in self.schulungen))

    @property
    def juleis_per_slot(self) -> float:  # for time estimates
        return len(self.juleis)/self.total_capacity

    def __init__(
            self,
            name: str,
            juleis: Iterable[JuLei],
            schulungen: Iterable[Schulung],
            scores: dict[Schulung, dict[JuLei, int]] | None = None
        ):
        self.name = name
        self.juleis = list(juleis)
        self.schulungen = list(schulungen)
        self.juleis_by_id = {j.id: j for j in juleis}
        self.schulungen_by_id = {s.id: s for s in schulungen}
        self._sort_juleis_and_schulungen()  # optional
        if scores is None:
            scores = self._get_random_scores()
        self.scores = scores

    def _sort_juleis_and_schulungen(self):
        """
        Sorting the JuLeis and Schulungen does not change the end result,
        but it changes the allocation process and can make it easier to follow.
        """
        self.juleis.sort(key=lambda j: (not j.from_bw, len(j.wishes)))

        estimated_demand = {s: -s.capacity for s in self.schulungen}
        for wished_schulungen in self.get_wishes_of_juleis().values():
            for wished_schulung in wished_schulungen:
                estimated_demand[wished_schulung] += 1
        self.schulungen.sort(key=lambda s:(estimated_demand[s], s.capacity))

    def _get_random_scores(self) -> dict[Schulung, dict[JuLei, int]]:
        unique_scores = list(range(len(self.juleis)))
        scores: dict[Schulung, dict[JuLei, int]] = defaultdict(dict)
        for s in self.schulungen:
            shuffle(unique_scores)
            for julei, score in zip(self.juleis, unique_scores):
                scores[s][julei] = score
        return scores

    def get_wishes_of_juleis(self) -> dict[JuLei, list[Schulung]]:
        wishes_of_juleis: dict[JuLei, list[Schulung]] = defaultdict(list)
        for julei in self.juleis:
            for schulungs_id in julei.wishes:
                wishes_of_juleis[julei].append(self.schulungen_by_id[schulungs_id])
        return wishes_of_juleis
