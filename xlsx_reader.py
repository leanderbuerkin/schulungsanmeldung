from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet

from data_structures import InputData

def read_from_xlsx(xlsx_path: Path) -> InputData:
    xlsx = load_workbook(xlsx_path)
    events = _get_events(xlsx)
    seekers = _get_seekers(xlsx, events)
    random_order = 
    return InputData(
        name = xlsx_path.stem,
        events = events,
        seekers = seekers,
        random_order = 


    )
