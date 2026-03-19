
from collections import defaultdict
from collections.abc import Iterable
import json
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook

from data import Data, JuLei, Schulung
from xlsx_config import JULEI_SHEET_NAME, SCHULUNGEN_SHEET_NAME, SCORES_SHEET_NAME, index_as_columns, index_as_rows

def _get_as_dict(cells: tuple[Any, ...], keys: Iterable[str]) -> dict[str, Any]:
    as_dict: dict[str, Any] = dict()
    for i, key in enumerate(keys):
        value = json.loads(str(cells[i]))
        # JSON converts tuples to lists
        if isinstance(value, list):
            as_dict[key] = tuple(value) # pyright: ignore[reportUnknownArgumentType]
        else:
            as_dict[key] = value
    return as_dict

def _get_schulungen(xlsx: Workbook) -> list[Schulung]:
    rows = xlsx[SCHULUNGEN_SHEET_NAME].iter_rows(values_only=True)
    keys = [str(k) for k in next(rows)]
    schulungen_as_dicts: list[dict[str, Any]] = list()
    for row in rows:
        schulungen_as_dicts.append(_get_as_dict(row, keys))
    return [Schulung(**d) for d in schulungen_as_dicts]

def _get_juleis(xlsx: Workbook) -> list[JuLei]:
    columns = xlsx[JULEI_SHEET_NAME].iter_cols(values_only=True)
    keys = [str(k) for k in next(columns)]
    juleis_as_dicts: list[dict[str, Any]] = list()
    for column in columns:
        juleis_as_dicts.append(_get_as_dict(column, keys))
    return [JuLei(**d) for d in juleis_as_dicts]

def read(xlsx_path: Path) -> Data:
    xlsx = load_workbook(xlsx_path, True)
    schulungen = _get_schulungen(xlsx)
    juleis = _get_juleis(xlsx)
    scores: dict[Schulung, dict[JuLei, int]] = defaultdict(dict)
    for schulung, row in index_as_rows(schulungen).items():
        for julei, column in index_as_columns(juleis).items():
            scores[schulung][julei] = xlsx[SCORES_SHEET_NAME][column+row].value
    return Data(xlsx_path.stem, juleis, schulungen, scores)
