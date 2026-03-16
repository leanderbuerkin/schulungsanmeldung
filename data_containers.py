from dataclasses import dataclass

@dataclass
class JuLei:
    from_bw: bool
    wishes: list[int]
    allocated: int | None

type Capacity = int

@dataclass
class Problem:
    name: str
    juleis: list[JuLei]
    schulungen: list[Capacity]
