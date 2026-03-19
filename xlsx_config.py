from collections.abc import Iterable
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from input_data import Schulung, JuLei

class XLSX:
    FIRST_INDEX = 1
    JULEI_SHEET_NAME = "data--juleis"
    SCHULUNGEN_SHEET_NAME = "data--schulungen"
    SCORES_SHEET_NAME = "data--scores"

    FROM_BW_STRING = "Baden-Württemberger*in"
    NOT_FROM_BW_STRING = " "

    @staticmethod
    def get_new_workbook(first_sheet_title: str) -> Workbook:
        xlsx = Workbook()

        if len(xlsx.worksheets) > 0: # should always be True after creation
            first_sheet = xlsx.worksheets[0]
        else:
            first_sheet = xlsx.create_sheet()
        first_sheet.title = first_sheet_title
        first_sheet.append(["Feel free to write or delete something here!"])
        first_sheet.append(["This sheet is not read, overwritten or needed by the computer."])
        first_sheet.append(["Switch sheets by pressing STRG + (SHIFT) + TAB."])

        return xlsx

    @staticmethod
    def as_rows(
            schulungen: Iterable[Schulung],
            number_of_header_rows: int=1
        ) -> dict[Schulung, str]:
        """Only allows Schulungen to prevent confuse rows and columns."""

        rows: dict[Schulung, str] = dict()
        offset = XLSX.FIRST_INDEX + number_of_header_rows
        for i, schulung in enumerate(schulungen, offset):
            rows[schulung] = str(i)

        return rows

    @staticmethod
    def as_columns(
            juleis: Iterable[JuLei],
            number_of_header_columns: int=1
        ) -> dict[JuLei, str]:
        """Only allows JuLeis to prevent confuse rows and columns."""

        columns: dict[JuLei, str] = dict()
        offset = XLSX.FIRST_INDEX + number_of_header_columns
        for i, julei in enumerate(juleis, offset):
            columns[julei] = get_column_letter(i)

        return columns

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
