from collections.abc import Iterable
from os import makedirs
from pathlib import Path
from openpyxl.utils import get_column_letter

from allocator import JuLei, Schulung

DATA_DIRECTORY = Path("data")
makedirs(DATA_DIRECTORY, exist_ok=True)

FROM_BW_STRING = "Baden-Württemberger*in"

FIRST_INDEX_IN_XLSX = 1
NUMBER_OF_HEADER_COLUMNS = 1
NUMBER_OF_HEADER_ROWS = 1

SHEET_WITH_JULEI_DATA = "juleis"
SHEET_WITH_SCHULUNGS_DATA = "schulungen"
SHEET_WITH_SCORE_DATA = "scores"
INITIAL_SHEET = "initial"

COLUMN_WIDTH = 2.5  # guess

WHITE = "FFFFFF"
JULEI_FROM_BW_COLOR = "400080"
JULEI_NOT_FROM_BW_COLOR = "004080"
SCHULUNG_HEADER_COLOR = "000050"
FULL_SCHULUNG_HEADER_COLOR = "800000"

FULL_SCHULUNG_COLOR = "800020"
DENIED_WISH_COLOR = "800020"
HIGHLIGHT_COLOR = "FA00FA"
ALLOCATED_JULEI_COLOR = "CCFFCC"
ALLOCATION_COLOR = "008000"

def wish_from_bw_color(v: int) -> str:
    rgb = (min(215, 40+50*v), min(175, 50*v), min(255, 80+50*v))
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def wish_not_from_bw_color(v: int) -> str:
    rgb = (min(175, 50*v), min(215, 40+50*v), min(255, 80+50*v))
    return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def get_row_index(schulung: Schulung, schulungen: Iterable[Schulung], headers: bool=False) -> str:
    row_index = FIRST_INDEX_IN_XLSX + (NUMBER_OF_HEADER_ROWS if headers else 0)
    for s in schulungen:
        if schulung == s:
            break
        row_index += 1
    return str(row_index)

def get_column_index(julei: JuLei, juleis: Iterable[JuLei], headers: bool=False) -> str:
    column_index = FIRST_INDEX_IN_XLSX + (NUMBER_OF_HEADER_COLUMNS if headers else 0)
    for j in juleis:
        if julei == j:
            break
        column_index += 1
    return get_column_letter(column_index)

def get_cell_index(schulung: Schulung, julei: JuLei, schulungen: Iterable[Schulung], juleis: Iterable[JuLei], headers: bool=False) -> str:
    return get_column_index(julei, juleis, headers) + get_row_index(schulung, schulungen, headers)
