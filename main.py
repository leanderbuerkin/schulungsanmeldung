
from file_saver import save_to_new_xlsx
from random_problem_generator import generate_random_problem

problem = generate_random_problem(100, 1000)
xlsx_file_path = save_to_new_xlsx(problem, "initial")
