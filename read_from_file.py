
from pathlib import Path

from pandas import DataFrame, read_csv

from data_containers import JuLei, Schulung


def read_juleis(csv: Path) -> list[JuLei]:
    return [JuLei(row) for row in read_csv(csv).values]

def read_schulungen(csv: Path) -> list[Schulung]:
    return [Schulung(row) for row in read_csv(csv).values]

def read_preferences(csv: Path, number_of_schulungen: int, number_of_juleis: int) -> DataFrame:
    """The rows are the Schulungen and the columns are the JuLeis."""
    return read_csv(csv, nrows=number_of_schulungen, usecols=range(number_of_juleis),header=None)
