from collections.abc import Generator, Iterable
from time import time
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter

from data import JuLei, Schulung

FROM_BW_STRING = "Baden-Württemberger*in"
NOT_FROM_BW_STRING = " "

FIRST_INDEX_IN_XLSX = 1
COLUMN_WIDTH = 2.5  # guess
NUMBER_OF_HEADER_COLUMNS = 1
NUMBER_OF_HEADER_ROWS = 1

JULEI_SHEET_NAME = "data--juleis"
SCHULUNGEN_SHEET_NAME = "data--schulungen"
SCORES_SHEET_NAME = "data--scores"

class Colors:
    WHITE = "FFFFFF"

    SCHULUNG_HEADER = "000050"
    JULEI_FROM_BW_HEADER = "400080"
    JULEI_NOT_FROM_BW_HEADER = "004080"

    HIGHLIGHTED_WISH = "FA00FA"
    GRANTED_WISH = "008000"
    REJECTED_WISH = "800020"

    WISH_BRIGHTNESS = (0, 50, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170)
    WISH_FROM_BW_BASE_RGB = (40, 0, 80)
    WISH_NOT_FROM_BW_BASE_RGB = (0, 40, 80)

    @staticmethod
    def wish(brightness_level: int, from_bw: bool) -> str:
        brightness_level = max(0, min(len(Colors.WISH_BRIGHTNESS)-1, brightness_level))
        brightness = Colors.WISH_BRIGHTNESS[brightness_level]
        if from_bw:
            base = Colors.WISH_FROM_BW_BASE_RGB
        else:
            base = Colors.WISH_NOT_FROM_BW_BASE_RGB
        rgb: list[int] = list()
        for channel in base:
            rgb.append(max(0, min(255, channel+brightness)))
        return f"{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def get_new_workbook(first_sheet_title: str) -> Workbook:
        xlsx = Workbook()
        if len(xlsx.worksheets) == 0:  # should always be False after creation
            first_sheet = xlsx.create_sheet(first_sheet_title)
        else:
            first_sheet = xlsx.worksheets[0]
            first_sheet.title = first_sheet_title
        first_sheet.append(["Feel free to write or delete something here!"])
        first_sheet.append(["This sheet is not read, overwritten or needed by the computer."])
        first_sheet.append(["Switch sheets by pressing STRG + TAB."])
        return xlsx

def index_as_rows(schulungen: Iterable[Schulung]) -> dict[Schulung, str]:
    rows: dict[Schulung, str] = dict()
    offset = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_ROWS
    for i, schulung in enumerate(schulungen, offset):
        rows[schulung] = str(i)
    return rows

def index_as_columns(juleis: Iterable[JuLei]) -> dict[JuLei, str]:
    columns: dict[JuLei, str] = dict()
    offset = FIRST_INDEX_IN_XLSX + NUMBER_OF_HEADER_COLUMNS
    for i, julei in enumerate(juleis, offset):
        columns[julei] = get_column_letter(i)
    return columns

def get_sheet_generator(xlsx: Workbook) -> Generator[Worksheet]:
    start_time = time()
    sheet: Worksheet = xlsx.create_sheet(f"{time() - start_time:.6f}")
    while True:
        yield sheet
        sheet = xlsx.copy_worksheet(sheet)
        sheet.title = f"{time() - start_time:.6f}"
