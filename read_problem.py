
from pathlib import Path

from pandas import DataFrame, read_csv

from data_containers import JuLei, Problem, Schulung

def read_juleis(csv: Path) -> list[JuLei]:
    return [JuLei(row) for row in read_csv(csv).values]

def read_schulungen(csv: Path) -> list[Schulung]:
    return [Schulung(row) for row in read_csv(csv).values]

def read_problem(input: Path) -> Problem:
    schulungen = read_schulungen(input/"schulungen.csv")
    juleis = read_juleis(input/"juleis.csv")
    preferences = read_csv(input/"preferences.csv", nrows=len(schulungen), usecols=range(len(juleis)), header=None)
    allocations = DataFrame(index=range(len(schulungen)), columns=range(len(juleis)))
    return Problem(dict(input=input), juleis, schulungen, preferences, allocations)
