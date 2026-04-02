from enum import StrEnum

from openpyxl import Workbook
from openpyxl.utils import get_column_letter


FIRST_INDEX = 1
HEADER_INDIZES_COUNT = 1
FIRST_CONTENT_INDEX = FIRST_INDEX + HEADER_INDIZES_COUNT
COLUMN_WIDTH = 2.5

LOG_SHEET_NAME = "log"


class SheetNames(StrEnum):
    EVENTS = "events"
    SEEKERS = "seekers"
    RANKED_WISHES = "wishes"
    ORDERED_WISHES = "ordered-wishes-generated"
    RANKINGS = "rankings-generated"
    PARTICIPANTS = "participants-generated"


class Color(StrEnum):
    WHITE = "FFFFFF"

    EVENT_HEADER = "000050"
    SEEKERS_FROM_BW_HEADER = "400080"
    SEEKERS_NOT_FROM_BW_HEADER = "004080"

    SUCCESS = "008000"
    FAILURE = "C80000"
    UNCHECKED_FROM_BW = "CCAAFF"
    UNCHECKED_NOT_FROM_BW = "AACCFF"


def _get_indizes(amount: int) -> list[int]:
    offset = FIRST_CONTENT_INDEX
    return list(range(offset, offset + amount))

def get_row_indizes(amount: int) -> list[str]:
    return [str(i) for i in _get_indizes(amount)]

def get_column_indizes(amount: int) -> list[str]:
    return [get_column_letter(i) for i in _get_indizes(amount)]

def get_new_workbook() -> Workbook:
    xlsx = Workbook()

    if len(xlsx.worksheets) > 0: # should always be True after creation
        first_sheet = xlsx.worksheets[0]
    else:
        first_sheet = xlsx.create_sheet()
    first_sheet.append(["Switch sheets by pressing STRG + (SHIFT) + TAB."])

    return xlsx
