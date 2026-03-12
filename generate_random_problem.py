import csv
from os import makedirs
from pathlib import Path
from random import gauss
from faker import Faker

from data_containers import FROM_BAWUE_STRING, NOT_FROM_BAWUE_STRING

NUMBER_OF_SCHULUNGEN = 4
NUMBER_OF_JULEIS = 6
NUMBER_OF_JULEIS_FROM_BAWUE = 3
MAX_PARTICIPANTS_MIN = 6
MAX_PARTICIPANTS_MAX = 20

directory_path = Path(f"problems/random_{NUMBER_OF_SCHULUNGEN}_Schulungen_{NUMBER_OF_JULEIS}_Juleis")
makedirs(directory_path, exist_ok=True)

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

fake = Faker()
with open(directory_path/"juleis.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "From BaWue"])
    for index in range(NUMBER_OF_JULEIS):
        bawue_string = FROM_BAWUE_STRING
        if index >= NUMBER_OF_JULEIS_FROM_BAWUE:
            bawue_string = NOT_FROM_BAWUE_STRING
        writer.writerow([
            fake.name(),
            bawue_string
        ])

with open(directory_path/"schulungen.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["Schulungsnummer", "Name", "Max. Participants"])
    for index in range(NUMBER_OF_SCHULUNGEN):
        writer.writerow([
            f"FB{index:02d}",
            SAMPLE_NAMES_FOR_SCHULUNGEN[index%len(SAMPLE_NAMES_FOR_SCHULUNGEN)],
            max(MAX_PARTICIPANTS_MIN, min(MAX_PARTICIPANTS_MAX, int(gauss(12, 2))))
        ])

with open(directory_path/"preferences.csv", "w") as file:
    writer = csv.writer(file)
    for _ in range(NUMBER_OF_SCHULUNGEN):
        writer.writerow([gauss(50, 40) for _ in range(NUMBER_OF_JULEIS)])
