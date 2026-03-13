
from functools import partial
from os import makedirs
from pathlib import Path

from pandas import Series

from config import FROM_BAWUE_STRING, NOT_FROM_BAWUE_STRING, STRING_TO_MARK_ALLOCATIONS
from data_containers import Problem
from dataframe_image import export # pyright: ignore[reportUnknownVariableType, reportMissingTypeStubs]

def highlight(p: Problem, column: Series) -> list[str]:
    """Sadly, font-weight, font-size and border are not recognized by
    export(table_conversion="matplotlib")"""
    formatting: list[str] = [""] * len(column)
    column_index = int(str(column.name))
    for row_index in range(len(column)):
        schulung = p.schulungen[row_index]
        julei = p.juleis[column_index]
        if p.is_full(schulung):
            formatting[row_index] = "background-color: maroon; color: white"
        if not p.get_allocation(julei) is None:
            formatting[row_index] = "background-color: palegreen; color: black"
        if p.get_allocation(julei) == row_index:
            formatting[row_index] = "background-color: darkgreen; color: white"
    return formatting

def save_as_image(p: Problem, output_path_without_file_extension: Path) -> None:
    output_path = output_path_without_file_extension.with_suffix(".png")
    makedirs(output_path.parent, exist_ok=True)
    output = p.preferences.style
    for julei in p.juleis:
        if julei.from_bawue:
            output = output.background_gradient(subset=[julei.column_index], cmap="Blues")
        else:
            output = output.background_gradient(subset=[julei.column_index], cmap="Purples")
    output = output.highlight_null(color="white")
    output = output.format('{:.0%}', na_rep="")
    output = output.apply(partial(highlight, p))
    output = output.relabel_index([str(s.max_participants) for s in p.schulungen], axis=0)
    output = output.relabel_index([FROM_BAWUE_STRING if j.from_bawue else NOT_FROM_BAWUE_STRING for j in p.juleis], axis=1)
    export(output, str(output_path), table_conversion="matplotlib", max_cols=-1, max_rows=-1) # pyright: ignore[reportArgumentType]

def save_as_csv(p: Problem, output_path_without_file_extension: Path) -> None:
    output_path = output_path_without_file_extension.with_suffix(".csv")
    makedirs(output_path.parent, exist_ok=True)
    output = p.preferences.copy(True).astype(str).replace('nan', '')
    for julei in p.juleis:
        row_index = p.get_allocation(julei)
        if not row_index is None:
            output.iloc[row_index, julei.column_index] = STRING_TO_MARK_ALLOCATIONS
    output.to_csv(output_path, index=False, header=False)
