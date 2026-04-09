from allocator import get_solution
from random_data_generator import Stats, generate_random_input_data
from xlsx_config import OUTPUT_DIRECTORY_PATH
from xlsx_reader import read_xlsx
from xlsx_writer import save_to_xlsx

def generate_random_and_save():
    stats = Stats(
        events_count=100,
        seekers_count=1000,
        seekers_from_bw_in_percent=80,
        events_capacity_min=8,
        events_capacity_max =12,
        wishes_per_rank_min=1,
        wishes_per_rank_max=10,
        wishes_ranks_count=3
    )
    ranked_wishes = generate_random_input_data(stats)
    participants_lists = get_solution(ranked_wishes)
    save_to_xlsx(ranked_wishes, participants_lists, stats)

def read_and_solve_example():
    ranked_wishes = read_xlsx(OUTPUT_DIRECTORY_PATH/"2026_04_09_example.xlsx")
    participants_lists = get_solution(ranked_wishes)
    save_to_xlsx(ranked_wishes, participants_lists, None, "2026_04_09_example")

generate_random_and_save()
read_and_solve_example()
