
from os import makedirs
from pathlib import Path

GENERATE_LOGS = True

DATA_DIRECTORY = Path("data")
makedirs(DATA_DIRECTORY, exist_ok=True)

FROM_BW_STRING = "BW"
NOT_FROM_BW_STRING = "Not BW"

STRING_TO_MARK_ALLOCATIONS = "T"
