from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from pandas import DataFrame

FROM_BAWUE_STRING = "FROM BAWUE"
NOT_FROM_BAWUE_STRING = "NOT " + FROM_BAWUE_STRING

@dataclass
class JuLei:
    name: str
    from_bawue: bool
    @property
    def as_strings(self) -> tuple[str, str]:
        return self.name, FROM_BAWUE_STRING if self.from_bawue else NOT_FROM_BAWUE_STRING

@dataclass
class Schulung:
    name: str
    participants_maximum: int
    @property
    def as_strings(self) -> tuple[str, str]:
        return self.name, str(self.participants_maximum)

@dataclass
class Preferences:
    file_information: dict[str, Any]
    juleis: list[JuLei]
    schulungen: list[Schulung]
    preferences: DataFrame


