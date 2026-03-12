from __future__ import annotations
from dataclasses import dataclass
from os import makedirs
from pathlib import Path
from typing import cast
from numpy import float64, nan
from pandas import DataFrame, Series, isna, read_csv
from dataframe_image import export # pyright: ignore[reportUnknownVariableType, reportMissingTypeStubs]

# Ask GS, which value or error is better.
DEFAULT_MAX_PARTICIPANTS_PER_SCHULUNG = 10

FROM_BAWUE_STRING = "FROM BAWUE"
NOT_FROM_BAWUE_STRING = "NOT " + FROM_BAWUE_STRING

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
    input: Path
    output: Path
    number_of_generated_files: int
    schulungen: list[Schulung]
    juleis: list[JuLei]
    preferences: DataFrame
    allocations: DataFrame

    def __init__(self, input: Path, output: Path) -> None:
        self.input = input
        self.output = output
        makedirs(self.output, exist_ok=True)
        self.number_of_generated_files = 0

        self.schulungen = list()
        for row_id, row in enumerate(read_csv(input/"schulungen.csv").values):
            max_participants = DEFAULT_MAX_PARTICIPANTS_PER_SCHULUNG
            if not isna(row[2]):
                max_participants = row[2]
            self.schulungen.append(Schulung(row_id, row[0], row[1], max_participants))

        self.juleis = list()
        for row_id, row in enumerate(read_csv(input/"juleis.csv").values):
            self.juleis.append(JuLei(row_id, row[0], row[1] == FROM_BAWUE_STRING))

        self.allocations = DataFrame(False, index=range(len(self.schulungen)), columns=range(len(self.juleis)), dtype=bool)
        self.read_preferences(input)
        self.remove_negative_preferences()
        self.scale_each_preference_column_to_one()

    def read_preferences(self, input: Path) -> None:
        self.preferences = read_csv(input/"preferences.csv", nrows=len(self.schulungen), usecols=range(len(self.juleis)), dtype=float64, header=None)
        self.save_as_image("unchanged")

    def remove_negative_preferences(self) -> None:
        self.preferences[self.preferences < 0] = nan
        self.save_as_image("removed_negative_values")

    def scale_each_preference_column_to_one(self) -> None:
        self.preferences = self.preferences / self.preferences.sum(axis=0)
        self.save_as_image("scaled_each_column_to_one")

    def save_as_image(self, file_name: str) -> None:
        def highlight(column: Series) -> list[str]:
            formatting: list[str] = [""] * len(column)
            column_index = int(str(column.name))
            for row_index in range(len(column)):
                schulung = self.schulungen[row_index]
                julei = self.juleis[column_index]

                if self.is_full(schulung):
                    formatting[row_index] = "background-color: maroon; color: white"

                if isinstance(self.get_allocation(julei), int):
                    formatting[row_index] = "background-color: palegreen; color: black"
                if self.get_allocation(julei) == row_index:
                    formatting[row_index] = "background-color: darkgreen; color: white"
            return formatting

        output = self.preferences[:].style
        output = output.background_gradient(subset=[j.column_index for j in self.juleis if j.from_bawue], cmap="Blues")
        output = output.background_gradient(subset=[j.column_index for j in self.juleis if not j.from_bawue], cmap="Purples")
        output = output.highlight_null(color="white")
        output = output.format('{:.0%}', na_rep="")
        output = output.apply(highlight)
        # output = output.relabel_index([s.schulungsnummer for s in self.schulungen], axis=0)
        # output = output.relabel_index([j.name[:4] for j in self.juleis], axis=1)
        # todo: change to another format.
        self.number_of_generated_files += 1
        output_file_path = self.output / f"{self.number_of_generated_files:02d}_{file_name}.png"
        export(output, str(output_file_path), table_conversion="matplotlib") # pyright: ignore[reportArgumentType]

    def get_preferences(self, schulung: Schulung | None=None, julei: JuLei | None=None) -> DataFrame | Series | float64:
        match schulung, julei:
            case Schulung(row_index=row_index), JuLei(column_index=column_index):
                return cast(float64, self.preferences.iloc[row_index,column_index])
            case Schulung(row_index=row_index), None:
                return self.preferences.iloc[row_index,:]
            case None, JuLei(column_index=column_index):
                return self.preferences.iloc[:,column_index]
            case None, None:
                return self.preferences

    def add_allocation(self, schulung: Schulung, julei: JuLei) -> None:
        self.allocations.iloc[schulung.row_index, julei.column_index] = True

    def get_allocation(self, julei: JuLei) -> int | None:
        for value_index, value in enumerate(self.allocations.iloc[:, julei.column_index]):
            if value:
                return value_index
        return None

    def is_full(self, schulung: Schulung) -> bool:
        return self.allocations.iloc[schulung.row_index,:].sum() >= schulung.max_participants


Problem(Path("problems/random_4_Schulungen_6_Juleis"),
        Path("solutions/random_4_Schulungen_6_Juleis"))
