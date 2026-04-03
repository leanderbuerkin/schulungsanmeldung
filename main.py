

from _00_stats_to_input_data import generate_random_input_data
from _01_input_data_to_parameters import choose_parameters
from _02_parameters_to_solution import get_solution
from data_structures import Stats
from xlsx_writer import save_to_xlsx


stats = Stats(
    events_count=100,
    seekers_count=1000,
    seekers_from_bw_in_percent=80,
    events_capacity_range=(8, 12),
    wishes_count_range=(1, 10),
    wishes_ranks_count=3
)
input_data = generate_random_input_data(stats)

parameters = choose_parameters(input_data)
solution = get_solution(parameters)
save_to_xlsx(solution)
