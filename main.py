

from pathlib import Path

from _00_stats_to_input_data import generate_random_input_data
from _01_input_data_to_parameters import choose_parameters
from _02_parameters_to_solution import get_solution
from data_structures import Solution, Stats
from xlsx_reader import read_xlsx
from xlsx_writer import save_to_xlsx


# stats = Stats(
#     events_count=100,
#     seekers_count=1000,
#     seekers_from_bw_in_percent=80,
#     events_capacity_min=8,
#     events_capacity_max =12,
#     wishes_count_min=1,
#     wishes_count_max=10,
#     wishes_ranks_count=3
# )
# input_data = generate_random_input_data(stats)
# 
# parameters = choose_parameters(input_data)
# solution = get_solution(parameters)
# save_to_xlsx(solution)


read_solution = read_xlsx(Path("output/old_100_events__1000_seekers__8_to_12_slots__1_to_10_wishes__3_ranks.xlsx"))
match read_solution:
    case Solution():
        save_to_xlsx(read_solution)
        print(read_solution.parameters.input_data.stats)
    case _:
        pass
