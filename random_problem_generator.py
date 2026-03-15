from csv import writer
from os import makedirs
from pathlib import Path
from random import randint

from config import PROBLEMS_DIRECTORY, SOLUTIONS_DIRECTORY
from config import SCHULUNGEN_FILE_NAME, JULEI_FILE_NAME, PRIORITIES_FILE_NAME
from config import NUMBER_OF_PRIORITY_LEVELS
from config import FROM_BW_STRING, NOT_FROM_BW_STRING

def generate_random_problem(
        number_of_schulungen: int,
        number_of_juleis: int,
        juleis_from_bw_in_percent: int = 80,
        max_juleis_range: tuple[int, int] = (6, 14),
        
    ) -> tuple[Path, Path]:

    problem_path = Path(PROBLEMS_DIRECTORY/"random"/
        f"{number_of_schulungen}_Schulungen_{number_of_juleis}_Juleis"
    )
    makedirs(problem_path, exist_ok=True)
    solution_path = Path(SOLUTIONS_DIRECTORY/"random"/
        f"{number_of_schulungen}_Schulungen_{number_of_juleis}_Juleis"
    )
    makedirs(solution_path, exist_ok=True)

    number_of_juleis_from_bw = (number_of_juleis*juleis_from_bw_in_percent)//100
    number_of_juleis_not_from_bw = number_of_juleis-number_of_juleis_from_bw

    with open(problem_path/SCHULUNGEN_FILE_NAME, "w") as file:
        output = writer(file)
        output.writerow([randint(*max_juleis_range) for _ in range(number_of_schulungen)])

    with open(problem_path/JULEI_FILE_NAME, "w") as file:
        output = writer(file)
        output.writerow([FROM_BW_STRING]*number_of_juleis_from_bw +
                        [NOT_FROM_BW_STRING]*number_of_juleis_not_from_bw)

    with open(problem_path/PRIORITIES_FILE_NAME, "w") as file:
        output = writer(file)
        for _ in range(number_of_juleis):
            row: list[str] = list()
            for _ in range(number_of_schulungen):
                # NUMBER_OF_PRIORITY_LEVELS is included -> cells with this number will be empty.
                priority_level = randint(0, NUMBER_OF_PRIORITY_LEVELS)
                if priority_level in range(NUMBER_OF_PRIORITY_LEVELS):
                    row.append(str(priority_level))
                else:
                    row.append("")
            output.writerow(row)

    return problem_path, solution_path
