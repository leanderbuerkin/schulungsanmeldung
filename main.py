
# todo: Add tests (is really everything unchanged after writing and reading xlsx)

from os import makedirs
from pathlib import Path

from allocator import find_best_allocation
from generators import generate_random_input_data
from xlsx import XLSX, XLSXPlotter, XLSXWriter



DATA_DIRECTORY = Path("data")

input_data = generate_random_input_data(40, 200, 50, 3, 5, 4, 0, 3)

solution = find_best_allocation(input_data)

xlsx = XLSX.get_new_workbook(solution.name)
XLSXWriter.add_data_to_xlsx(input_data, xlsx)
XLSXWriter.add_log_file_to_xlsx(input_data.log_file_path, xlsx)
XLSXPlotter.add_plot_to_xlsx(xlsx, solution)

makedirs(DATA_DIRECTORY, exist_ok=True)
xlsx.save(DATA_DIRECTORY/f"{solution.name}.xlsx")
input_data = generate_random_input_data(20, 300, 80, 8, 12, 0, 50)
