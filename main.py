
from allocators import allocate
from file_saver import save_to_new_xlsx
from random_problem_generator import generate_random_problem

# TODO: Maybe move into problem
# TODO: BW

problem = generate_random_problem(2, 20, (1, 1), 80, (1,2))
xlsx_file_path = save_to_new_xlsx(problem, "initial")

problem = allocate(problem, xlsx_file_path)
