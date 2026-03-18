from collections.abc import Generator, Iterable
from dataclasses import dataclass
from random import shuffle

type UniqueJuLeiId = int
type UniqueSchulungsId = int

@dataclass(frozen=True)
class JuLei:
    id: UniqueJuLeiId
    from_bw: bool
    wishes: tuple[UniqueSchulungsId, ...]

@dataclass(frozen=True)
class Schulung:
    id: UniqueSchulungsId
    capacity: int

class Allocator:
    # Given
    name: str
    juleis: list[JuLei]
    schulungen: list[Schulung]

    # Given or Generated
    scores: dict[Schulung, dict[JuLei, int]]

    # Generated
    participants: dict[Schulung, list[JuLei]]
    juleis_by_id: dict[UniqueJuLeiId, JuLei]
    schulungen_by_id: dict[UniqueSchulungsId, Schulung]

    @property
    def total_capacity(self) -> int:
        return sum((s.capacity for s in self.schulungen))

    @property
    def juleis_per_slot(self) -> float:
        return len(self.juleis)/self.total_capacity

    def _estimate_demand(self, schulung: Schulung) -> int:
        return sum((j.wishes.count(schulung.id) for j in self.juleis)) - schulung.capacity

    def __init__(self, name: str, juleis: Iterable[JuLei], schulungen: Iterable[Schulung],
                 scores: dict[Schulung, dict[JuLei, int]] | None = None):
        """If julei, schulungen and scores are given, the result should always be the same."""
        self.name = name
        # the order does not change the end result,
        # but it makes it easier to read and it changes the allocation process.
        self.juleis = sorted(juleis, key=lambda j: (not j.from_bw, len(j.wishes)))
        self.juleis_by_id = {j.id: j for j in self.juleis}
        self.schulungen = sorted(schulungen, key=lambda s: (self._estimate_demand(s), s.capacity))
        self.schulungen_by_id = {s.id: s for s in self.schulungen}

        if scores is None:
            unique_scores = list(range(len(self.juleis)))
            self.scores = {s: dict() for s in schulungen}
            for s in schulungen:
                shuffle(unique_scores)
                self.scores[s] = {j: v for j, v in zip(self.juleis, unique_scores)}
        else:
            self.scores = scores

        for _ in self.set_participants():
            pass

    def get_allocation(self, julei: JuLei) -> Schulung | None:
        for schulung, allocated_juleis in self.participants.items():
            if julei in allocated_juleis:
                return schulung
        return None

    def is_full(self, schulung: Schulung) -> bool:
        return len(self.participants[schulung]) >= schulung.capacity

    def _get_wishes_of_juleis(self) -> dict[JuLei, list[Schulung]]:
        wishes_of_juleis: dict[JuLei, list[Schulung]] = dict()
        for julei in self.juleis:
            wishes_of_juleis[julei] = [self.schulungen_by_id[s_id] for s_id in julei.wishes]
        return wishes_of_juleis

    def _pop_least_fitting_julei(self, schulung: Schulung) -> JuLei:
        self.participants[schulung] = sorted(self.participants[schulung], key=lambda j: self.scores[schulung][j])
        least_fitting_julei = self.participants[schulung][0]
        for julei in self.participants[schulung]:
            if not julei.from_bw:  # first julei not from Baden-Württemberg
                least_fitting_julei = julei
                break
        self.participants[schulung].remove(least_fitting_julei)
        return least_fitting_julei

    def _update_participants(self, schulung: Schulung, julei: JuLei) -> JuLei | None:
        self.participants[schulung].append(julei)
        if len(self.participants[schulung]) > schulung.capacity:
            return self._pop_least_fitting_julei(schulung)

    def set_participants(self) -> Generator[tuple[Schulung, list[JuLei], JuLei | None]]:
        self.participants = {s: list() for s in self.schulungen}
        unchecked_wishes = self._get_wishes_of_juleis()
        for julei in unchecked_wishes.keys():
            if not(self.get_allocation(julei) is None):
                continue
            while not(julei is None) and len(unchecked_wishes[julei]) > 0:
                best_schulung = unchecked_wishes[julei].pop(0)
                julei = self._update_participants(best_schulung, julei)
                yield best_schulung, self.participants[best_schulung], julei
