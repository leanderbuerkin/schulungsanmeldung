from dataclasses import dataclass
from pathlib import Path

type JuLeiId = int
type SchulungsId = int

@dataclass(frozen=True)
class JuLei:
    id: JuLeiId
    from_bw: bool
    wishes: list[SchulungsId]

@dataclass(frozen=True)
class Schulung:
    id: SchulungsId
    capacity: int
    scores: dict[JuLeiId, int]

@dataclass
class Problem:
    name: str
    output_directory: Path
    juleis: dict[JuLeiId, JuLei]
    schulungen: dict[SchulungsId, Schulung]
    participants: dict[SchulungsId, list[JuLeiId]]
    remaining_wishes: dict[JuLeiId, list[SchulungsId]]

    def is_allocated(self, julei: JuLei) -> bool:
        for participants_ids in self.participants.values():
            for participant_id in participants_ids:
                if participant_id == julei.id:
                    return True
        return False
