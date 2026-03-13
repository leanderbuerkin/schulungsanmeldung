
from pathlib import Path

from numpy import float64
from pandas import DataFrame, isna, read_csv

from config import MAX_PARTICIPANTS_PER_SCHULUNG_DEFAULT, FROM_BAWUE_STRING
from config import JULEI_FILE_NAME, PREFERENCES_FILE_NAME, SCHULUNGEN_FILE_NAME
from data_containers import JuLei, Problem, Schulung

def read_from_csv(input: Path) -> Problem:
    schulungen: list[Schulung] = list()
    for row_id, row in enumerate(read_csv(input/SCHULUNGEN_FILE_NAME).values):
        max_participants = MAX_PARTICIPANTS_PER_SCHULUNG_DEFAULT
        if not isna(row[2]):
            max_participants = row[2]
        schulungen.append(Schulung(row_id, row[0], row[1], max_participants))

    juleis: list[JuLei] = list()
    for row_id, row in enumerate(read_csv(input/JULEI_FILE_NAME).values):
        juleis.append(JuLei(row_id, row[0], row[1] == FROM_BAWUE_STRING))

    allocations = DataFrame(False, index=range(len(schulungen)), columns=range(len(juleis)), dtype=bool)
    preferences = read_csv(input/PREFERENCES_FILE_NAME, nrows=len(schulungen), usecols=range(len(juleis)), dtype=float64, header=None)

    return Problem(schulungen, juleis, preferences, allocations)
