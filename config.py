
from pathlib import Path

SCHULUNGEN_FILE_NAME = "schulungen.csv"
JULEI_FILE_NAME = "juleis.csv"
PREFERENCES_FILE_NAME = "preferences.csv"

PROBLEMS_DIRECTORY = Path("problems")
SOLUTIONS_DIRECTORY = Path("solutions")

# Ask GS, which value or error is better.
MAX_PARTICIPANTS_PER_SCHULUNG_DEFAULT = 10

FROM_BAWUE_STRING = "BAWUE"
NOT_FROM_BAWUE_STRING = "NOT " + FROM_BAWUE_STRING

STRING_TO_MARK_ALLOCATIONS = "True"
