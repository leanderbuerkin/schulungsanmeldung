
from os import makedirs
from pathlib import Path

DATA_DIRECTORY = Path("data")
makedirs(DATA_DIRECTORY, exist_ok=True)

FROM_BW_STRING = "BW"
NOT_FROM_BW_STRING = "Not BW"

STRING_FOR_ALLOCATIONS = " "
