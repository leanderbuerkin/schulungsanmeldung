from os import makedirs
from time import gmtime, strftime, time

from allocators import allocate_by_priority
from file_reader import read_from_csv
from file_saver import save_as_image, save_as_csv
from random_problem_generator import generate_random_problem

# TODO: Write test for Reallocating of JuLeis to fit all

problem_path, solution_path = generate_random_problem(25, 50, 80, 1, 5)
# problem_path, solution_path = generate_random_problem(2, 4, 80, 1, 5)
# problem_path, solution_path = generate_random_problem(100, 1000)

start_time = time()
makedirs(solution_path, exist_ok=True)
with open(solution_path/"log.md", "w") as f:
    f.write("# Elapsed Times\n\n")

def log_time(old_time: float, title:str) -> float:
    with open(solution_path/"log.md", "a") as f:
        f.write(f"{strftime("%H:%M:%S", gmtime(time()-old_time))}: {title}\n")
    return time()

problem = read_from_csv(problem_path)
current_time = log_time(start_time, "read_csv")

step_number = 0
for problem, message in allocate_by_priority(problem):
    file_name = f"{step_number:03d}_{message}_score_{problem.score}"
    current_time = log_time(current_time, message)
    save_as_csv(problem, solution_path/"csvs"/file_name)
    current_time = log_time(current_time, f"saving_csv_{file_name}")
    save_as_image(problem, solution_path/"images"/file_name)
    current_time = log_time(current_time, f"saving_image_{file_name}")
    step_number += 1
# file_name = f"000_solution_score_{problem.score}"
# save_as_image(problem, solution_path/"images"/file_name)
# current_time = log_time(current_time, f"saving_image_{file_name}")
