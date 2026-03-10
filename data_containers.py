from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from numpy import ndarray
from pandas import DataFrame, isna

# It would be better to raise an error
# But maybe this is not even issue in Odoo
DEFAULT_MAX_PARTICIPANTS_PER_SCHULUNG = 10

FROM_BAWUE_STRING = "FROM BAWUE"
NOT_FROM_BAWUE_STRING = "NOT " + FROM_BAWUE_STRING

@dataclass
class JuLei:
    name: str
    from_bawue: bool
    @property
    def as_strings(self) -> tuple[str, str]:
        return self.name, FROM_BAWUE_STRING if self.from_bawue else NOT_FROM_BAWUE_STRING

    def __init__(self, data: ndarray) -> None:
        self.name = data[0]
        self.from_bawue = False if data[1] == NOT_FROM_BAWUE_STRING else True

@dataclass
class Schulung:
    name: str
    max_participants: int
    @property
    def as_strings(self) -> tuple[str, str]:
        return self.name, str(self.max_participants)

    def __init__(self, data: ndarray) -> None:
        self.name = data[0]
        self.max_participants = DEFAULT_MAX_PARTICIPANTS_PER_SCHULUNG
        if not isna(data[1]):
            self.max_participants = data[1]

@dataclass
class Preferences:
    file_information: dict[str, Any]
    juleis: list[JuLei]
    schulungen: list[Schulung]
    preferences: DataFrame


