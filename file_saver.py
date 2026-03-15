"""
Not using datafrems-image because it does not allow to set edgecolors and fonts
and is tidious to work with.
"""
from csv import writer
from os import makedirs
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.table import Table

from config import FROM_BW_STRING, NOT_FROM_BW_STRING, NUMBER_OF_PRIORITY_LEVELS, STRING_TO_MARK_ALLOCATIONS
from data_containers import Problem

def _get_row_for_csv(p: Problem, index_julei: int) -> list[str]:
    row: list[str] = [""]*len(p.schulung_max_juleis)

    for priority_level, indizes_schulungen in enumerate(p.julei_priorities[index_julei]):
        for index_schulung in indizes_schulungen:
            row[index_schulung] = str(priority_level)

    allocated_schulung_index = p.julei_allocations[index_julei]
    if allocated_schulung_index is not None:
        row[allocated_schulung_index] = STRING_TO_MARK_ALLOCATIONS

    if p.julei_from_bw[index_julei]:
        row = [FROM_BW_STRING] + row
    else:
        row = [NOT_FROM_BW_STRING] + row
    return row

def save_as_csv(p: Problem, output_path_without_file_extension: Path) -> None:
    output_path = output_path_without_file_extension.with_suffix(".csv")
    makedirs(output_path.parent, exist_ok=True)
    with open(output_path, "w") as file:
        output = writer(file)
        output.writerow(["Max. JuLeis:"] + [str(n) for n in p.schulung_max_juleis])
        for index_julei in range(len(p.julei_from_bw)):
            output.writerow(_get_row_for_csv(p, index_julei))


FONT_SIZE = 100
FIRST_COLUMN_WIDTH_MULTIPLIER = 5

def save_as_image(p: Problem, output_path_without_file_extension: Path) -> None:
    output_path = output_path_without_file_extension.with_suffix(".png")
    makedirs(output_path.parent, exist_ok=True)

    number_of_columns = len(p.schulung_max_juleis) + FIRST_COLUMN_WIDTH_MULTIPLIER
    number_of_rows = len(p.julei_from_bw) + 1

    cell_width = 1 / number_of_columns
    cell_height = 1 / number_of_rows

    _, ax = plt.subplots(figsize=(number_of_columns, number_of_rows)) # pyright: ignore[reportUnknownMemberType]
    ax.set_axis_off()
    table = Table(ax)

    table.add_cell( # pyright: ignore[reportUnknownMemberType]
        row=0,
        col=0,
        width=cell_width*FIRST_COLUMN_WIDTH_MULTIPLIER,
        height=cell_height,
        text="Max. JuLeis:",
        facecolor="darkblue",
        #edgecolor='none'
    ).set_text_props(color='white', weight='bold', size=FONT_SIZE)

    for index_schulung, max_juleis in enumerate(p.schulung_max_juleis):
        table.add_cell( # pyright: ignore[reportUnknownMemberType]
            row=0,
            col=index_schulung+1,
            width=cell_width,
            height=cell_height,
            text=str(max_juleis),
            loc="center",
            facecolor="darkblue",
            #edgecolor='none'
        ).set_text_props(color='white', weight='bold', size=FONT_SIZE)

    for index_julei, from_bw in enumerate(p.julei_from_bw):
        if from_bw:
            facecolor = ('blue')
        else:
            facecolor = ('purple')
        table.add_cell( # pyright: ignore[reportUnknownMemberType]
            row=index_julei+1,
            col=0,
            width=cell_width*FIRST_COLUMN_WIDTH_MULTIPLIER,
            height=cell_height,
            text=FROM_BW_STRING if from_bw else NOT_FROM_BW_STRING,
            facecolor=facecolor,
            #edgecolor='none'
        ).set_text_props(color='white', weight='bold', size=FONT_SIZE)  #, rotation=90

    for index_julei, priorities in enumerate(p.julei_priorities):
        for priority_level, indizes_schulungen in enumerate(priorities):
            for index_schulung in indizes_schulungen:
                if p.julei_allocations[index_julei] == index_schulung:
                    facecolor = 'lime'
                elif p.is_full(index_schulung):
                    facecolor = ('red', 0.5)
                elif p.julei_allocations[index_julei] is not None:
                    facecolor = ('lime', 0.3)
                elif p.julei_from_bw[index_julei]:
                    facecolor = ('blue', 0.4*(1-priority_level/NUMBER_OF_PRIORITY_LEVELS))
                else:
                    facecolor = ('purple', 0.4*(1-priority_level/NUMBER_OF_PRIORITY_LEVELS))


                table.add_cell( # pyright: ignore[reportUnknownMemberType]
                    row=index_julei+1,
                    col=index_schulung+1,
                    width=cell_width,
                    height=cell_height,
                    text=str(priority_level),
                    loc="center",
                    facecolor=facecolor,
                    #edgecolor='none'
                ).set_text_props(size=FONT_SIZE)

    ax.add_table(table)
    plt.savefig(output_path, bbox_inches="tight", pad_inches=0, dpi=20) # pyright: ignore[reportUnknownMemberType]
    plt.close('all')
