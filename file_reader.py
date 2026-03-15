
from csv import reader
from pathlib import Path

from config import FROM_BW_STRING, NUMBER_OF_PRIORITY_LEVELS
from config import JULEI_FILE_NAME, PRIORITIES_FILE_NAME, SCHULUNGEN_FILE_NAME
from data_containers import PriorityLevelsOfOneJuLei, Problem

def read_from_csv(input_path: Path) -> Problem:
    with open(input_path/SCHULUNGEN_FILE_NAME, "r") as schulungen_file:
        schulung_max_juleis = [int(n) for n in next(reader(schulungen_file))]
    with open(input_path/JULEI_FILE_NAME, "r") as juleis_file:
        julei_from_bw = [s == FROM_BW_STRING for s in next(reader(juleis_file))]

    julei_priorities: list[PriorityLevelsOfOneJuLei] = list()
    with open(input_path/PRIORITIES_FILE_NAME, "r") as priorities_file:
        for priorities_of_julei in reader(priorities_file):
            priorities_by_level: PriorityLevelsOfOneJuLei = [set() for _ in range(NUMBER_OF_PRIORITY_LEVELS)]
            for index_schulung, priority_level_as_str in enumerate(priorities_of_julei):
                if priority_level_as_str in (str(i) for i in range(NUMBER_OF_PRIORITY_LEVELS)):
                    priorities_by_level[int(priority_level_as_str)].add(index_schulung)
            julei_priorities.append(priorities_by_level)
    return Problem(schulung_max_juleis, julei_from_bw, julei_priorities, [None]*len(julei_from_bw))
