from __future__ import annotations
from collections.abc import Generator
from dataclasses import dataclass
from typing import cast
from numpy import float64
from pandas import DataFrame, Series, isna

@dataclass(frozen=True)
class JuLei:
    column_index: int
    name: str
    from_bawue: bool

@dataclass(frozen=True)
class Schulung:
    row_index: int
    schulungsnummer: str
    name: str
    max_participants: int

@dataclass
class Problem:
    schulungen: list[Schulung]
    juleis: list[JuLei]
    preferences: DataFrame
    allocations: DataFrame
    @property
    def score(self) -> int:
        satisfied_preferences = 0
        for julei in self.juleis:
            row_index = self.get_allocation(julei)
            if not row_index is None:
                schulung = self.schulungen[row_index]
                satisfied_preference = self.get_preference(schulung, julei)
                if not isna(satisfied_preference):
                    satisfied_preferences += satisfied_preference
        return int(satisfied_preferences)

    def get_preferences(self, key: Schulung | JuLei) -> Series:
        match key:
            case Schulung(row_index=row_index):
                return self.preferences.iloc[row_index,:]
            case JuLei(column_index=column_index):
                return self.preferences.iloc[:,column_index]

    def get_preference(self, schulung: Schulung, julei: JuLei) -> float64:
        return cast(float64, self.preferences.iloc[schulung.row_index,julei.column_index])

    def add_allocation(self, schulung: Schulung, julei: JuLei) -> None:
        self.allocations.iloc[schulung.row_index, julei.column_index] = True

    def remove_allocation(self, julei: JuLei) -> None:
        allocation_row_index = self.get_allocation(julei)
        if not allocation_row_index is None:
            self.allocations.iloc[allocation_row_index, julei.column_index] = False

    def get_allocation(self, julei: JuLei) -> int | None:
        for value_index, value in enumerate(self.allocations.iloc[:, julei.column_index]):
            if value:
                return value_index
        return None

    def get_participants(self, schulung: Schulung) -> Generator[JuLei]:
        for value_index, value in enumerate(self.allocations.iloc[schulung.row_index,:]):
            if value:
                yield self.juleis[value_index]

    def is_full(self, schulung: Schulung) -> bool:
        return self.allocations.iloc[schulung.row_index,:].sum() >= schulung.max_participants
