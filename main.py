from time import gmtime, strftime, time

from config import DATA_DIRECTORY
from data_containers import Problem
from file_saver import save_to_xlsx
from random_problem_generator import generate_random_problem
from allocator import allocate

def print_stats(p: Problem, start_time: float, work_worst_case: int, work_expected: int):
    total_processing_time = time()-start_time
    work_done = p.number_of_checked_allocations
    width_work_worst_case = len(str(work_worst_case))
    if work_done == 0:
        return
    print("-----------")
    print(f"Worst Case: {work_done} of {work_worst_case} " +
        f"({work_done*100/work_worst_case:.2f} %) in {strftime("%H:%M:%S", gmtime(total_processing_time))} " +
        f"-> Remaining time: {strftime("%H:%M:%S", gmtime((total_processing_time/work_done) * work_worst_case - total_processing_time))}"
    )
    print(f"Expected:   {work_done} of {work_expected:>{width_work_worst_case}} " +
        f"({work_done*100/work_expected:.2f} %) in {strftime("%H:%M:%S", gmtime(total_processing_time))} " +
        f"-> Remaining time: {strftime("%H:%M:%S", gmtime((total_processing_time/work_done) * work_expected - total_processing_time))}"
    )

problem = generate_random_problem(DATA_DIRECTORY, 50, 200, (8, 12), 80, (1, 5))
work_worst_case = problem.worst_case_final_number_of_checked_allocations
work_expected = problem.expected_final_number_of_checked_allocations
start_time = time()

time_before_allocation = time()
for julei in allocate(problem):
    print(f"Allocation took     {time() - time_before_allocation:.6f} s.")

    time_before_saving = time()
    save_to_xlsx(
        problem,
        f"{time()-start_time:.2f} s",
        [julei]
    )

    print(f"Saving to xlsx took {time() - time_before_saving:.6f} s.")
    print_stats(problem, start_time, work_worst_case, work_expected)

    time_before_allocation = time()

total_processing_time = time()-start_time
save_to_xlsx(problem, f"{total_processing_time:.2f} s")
print("Saving result...")
problem.save_to_file()
print("Finished")
