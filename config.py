
from os import makedirs
from pathlib import Path

DATA_DIRECTORY = Path("data")
makedirs(DATA_DIRECTORY, exist_ok=True)

FIRST_XLSX_SHEET = "original problem"

FROM_BW_STRING = "BW"
NOT_FROM_BW_STRING = "Not BW"
ALLOCATIONS_STRING = " "

FIRST_INDEX_IN_XLSX = 1
NUMBER_OF_HEADER_COLUMNS = 1
NUMBER_OF_HEADER_ROWS = 1
FIRST_CONTENT_COLUMN_INDEX = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_COLUMNS
FIRST_CONTENT_ROW_INDEX = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_ROWS

WIDTH_OF_ONE_DIGIT = 1.5  # guess

WHITE = "FFFFFF"
WISH_FROM_ALLOCATED_JULEI_COLOR = "BBFFBB"
ALLOCATION_COLOR = "00FF00"
TOP_ROW_COLOR = "000050"

JULEI_FROM_BW_COLOR = "400080"
JULEI_NOT_FROM_BW_COLOR = "004080"

def wish_from_bw_color(v: int) -> str:
    rgb = (min(215, 40+50*v), min(175, 50*v), min(255, 80+50*v))
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def wish_not_from_bw_color(v: int) -> str:
    rgb = (min(175, 50*v), min(215, 40+50*v), min(255, 80+50*v))
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
