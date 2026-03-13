import csv
from os import makedirs
from pathlib import Path
from random import gauss
from faker import Faker

from config import PROBLEMS_DIRECTORY, SOLUTIONS_DIRECTORY
from config import SCHULUNGEN_FILE_NAME, JULEI_FILE_NAME, PREFERENCES_FILE_NAME
from config import FROM_BAWUE_STRING, NOT_FROM_BAWUE_STRING

# The following list is AI generated
SAMPLE_NAMES_FOR_SCHULUNGEN = [
    "Team trivia contest",
    "Escape room challenge",
    "Scavenger hunt adventure", 
    "Board game tournament",
    "Cooking competition",
    "Karaoke battle night",
    "DIY craft workshop",
    "Relay races",
    "Improv comedy games",
    "Puzzle solving race",
    "Charades tournament",
    "Build the tallest tower",
    "Two truths and a lie",
    "Human knot challenge",
    "Photo scavenger hunt",
    "Minute to win it games",
    "Jeopardy-style quiz",
    "Pictionary battle",
    "Talent show competition",
    "Obstacle course relay",
    "Murder mystery dinner",
    "Beach volleyball tournament",
    "Kneeboard races",
    "Freeze dance party",
    "Sardines hide and seek",
    "Water balloon toss",
    "Egg drop challenge",
    "Blind drawing contest",
    "Newspaper fashion show",
    "Balloon pop relay",
    "Suction cup target practice"
]

def generate_random_problem(
        number_of_schulungen: int,
        number_of_juleis: int,
        juleis_from_bawue_in_percent: int = 80,
        max_participants_min: int = 6,
        max_participants_max: int = 14
    ) -> tuple[Path, Path]:
    problem_path = Path(PROBLEMS_DIRECTORY/"random"/
        f"{number_of_schulungen}_Schulungen_{number_of_juleis}_Juleis"
    )
    makedirs(problem_path, exist_ok=True)
    solution_path = Path(SOLUTIONS_DIRECTORY/"random"/
        f"{number_of_schulungen}_Schulungen_{number_of_juleis}_Juleis"
    )
    makedirs(solution_path, exist_ok=True)

    number_of_juleis_from_bawue = (number_of_juleis*juleis_from_bawue_in_percent)//100
    max_participants_mean = (max_participants_max + max_participants_min)//2
    # max_participants_deviation = (max_participants_max - max_participants_min)//8
    random_value = lambda: int(gauss(max_participants_mean))
    new_max_participants = lambda: max(max_participants_min, min(max_participants_max, random_value()))

    fake = Faker()
    with open(problem_path/JULEI_FILE_NAME, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "From BaWue"])
        for index in range(number_of_juleis):
            bawue_string = FROM_BAWUE_STRING
            if index >= number_of_juleis_from_bawue:
                bawue_string = NOT_FROM_BAWUE_STRING
            writer.writerow([
                fake.name(),
                bawue_string
            ])
    
    with open(problem_path/SCHULUNGEN_FILE_NAME, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Schulungsnummer", "Name", "Max. Participants"])
        for index in range(number_of_schulungen):
            writer.writerow([
                f"FB{index:02d}",
                SAMPLE_NAMES_FOR_SCHULUNGEN[index%len(SAMPLE_NAMES_FOR_SCHULUNGEN)],
                new_max_participants()
            ])
    
    with open(problem_path/PREFERENCES_FILE_NAME, "w") as file:
        writer = csv.writer(file)
        for _ in range(number_of_schulungen):
            writer.writerow([gauss(50, 40) for _ in range(number_of_juleis)])

    return problem_path, solution_path
