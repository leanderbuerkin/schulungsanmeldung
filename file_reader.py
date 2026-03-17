from collections import defaultdict
from collections.abc import Iterable
import json
from typing import Any
from openpyxl import Workbook

from allocator import Allocator, JuLei, Schulung
from config import get_cell_index
from config import SHEET_WITH_JULEI_DATA, SHEET_WITH_SCHULUNGS_DATA, SHEET_WITH_SCORE_DATA

def _get_row_as_dict(row: tuple[Any, ...], keys: Iterable[str]) -> dict[str, Any]:
    row_as_dict: dict[str, Any] = dict()
    for i, key in enumerate(keys):
        value = json.loads(str(row[i]))
        # JSON converts tuples to lists
        if isinstance(value, list):
            row_as_dict[key] = tuple(value) # pyright: ignore[reportUnknownArgumentType]
        else:
            row_as_dict[key] = value
    return row_as_dict

def _get_rows_as_dicts(xlsx_file: Workbook, sheet_name: str) -> list[dict[str, Any]]:
    keys = [str(k) for k in next(xlsx_file[sheet_name].iter_rows(values_only=True))]
    rows_as_dicts: list[dict[str, Any]] = list()
    for row in xlsx_file[sheet_name].iter_rows(2, values_only=True):
        rows_as_dicts.append(_get_row_as_dict(row, keys))
    return rows_as_dicts

def get_allocator_from_xlsx(xlsx_file: Workbook) -> Allocator:
    juleis_as_dicts = _get_rows_as_dicts(xlsx_file, SHEET_WITH_JULEI_DATA)
    juleis = [JuLei(**d) for d in juleis_as_dicts]

    schulungen_as_dicts = _get_rows_as_dicts(xlsx_file, SHEET_WITH_SCHULUNGS_DATA)
    schulungen = [Schulung(**d) for d in schulungen_as_dicts]

    scores: dict[Schulung, dict[JuLei, int]] = defaultdict(dict)
    for schulung in schulungen:
        for julei in juleis:
            cell_index = get_cell_index(schulung, julei, schulungen, juleis)
            scores[schulung][julei] = xlsx_file[SHEET_WITH_SCORE_DATA][cell_index].value

    return Allocator(
        xlsx_file.worksheets[0].title,
        juleis, schulungen, scores
    )
