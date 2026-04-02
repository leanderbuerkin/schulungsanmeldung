

from _00_stats_to_input_data import generate_random_input_data
from _01_input_data_to_parameters import choose_parameters
from _02_parameters_to_solution import get_solution
from data_structures import Stats


stats = Stats(
    events_count=100,
    seekers_count=10000,
    seekers_from_bw_in_percent=80,
    events_capacity_range=(10, 10),
    wishes_count_range=(100, 100),
    wishes_ranks_count=3
)

input_data = generate_random_input_data(stats)
parameters = choose_parameters(input_data, None)
solution = get_solution(parameters)
