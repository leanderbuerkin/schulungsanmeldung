from collections.abc import Iterable
from logging import DEBUG, basicConfig, debug, info
from time import gmtime, strftime, time

from data_structures import Event, InputData, Solution, State

class Logger:
    generated_solutions_count_max: int
    start_time: float
    time_after_last_state_update: float
    time_after_last_solution_update: float

    @staticmethod
    def remaining_steps(wishes: Iterable[tuple[Event, ...]]) -> int:
        """
        This very simple heuristic only takes the longest number of wishes into account
        because it assumes that the two following effects cancel out:
        If more seekers compete for less slots,
        more seekers are rejected and search simultaneously (-> less steps),
        but more wishes need to be checked (-> more steps).
    
        In the worst case, each step only one wish is checked and
        each seeker only fits at the last wish.
        So the remaining steps guess is sum(len(wishes)).
    
        Less steps are needed if wishes from multiple seekers are checked in one step.
    
        In the best case, all seekers get a fitting spot in the first step.
        So the remaining steps guess is 1.
    
        More steps are needed if multiple wishes of seekers must get checked.
        """
        return max(len(ws) for ws in wishes)

    def __init__(self, parameters: InputData, generated_solutions_count_max: int):
        self.generated_solutions_count_max = generated_solutions_count_max
        self.current_process_count = 0

        with open(parameters.log_file_path, "w") as potentially_filled_file:
            potentially_filled_file.write("")

        basicConfig(
            level=DEBUG,
            format="%(asctime)s %(msecs)03d ms %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S ",
            filename=parameters.log_file_path
        )
        seekers_count = len(parameters.seekers)
        events_count = len(parameters.events)
        average_wishes = parameters.wishes_count/seekers_count

        info(f"{22*"-"} Started Allocation {parameters.name} {22*"-"}")
        debug(
            f"{seekers_count} seekers with on average {average_wishes:.1f} wishes " +
            f"need to be allocated to {parameters.capacity_sum} slots of {events_count} events."
        )
        debug(f"At most {generated_solutions_count_max} trys are made to find the best solution.")

        self.start_time = time()
        self.time_after_last_state_update = time()
        self.time_after_last_solution_update = time()

    def log_state_update(self, finished_steps: int, state: State):
        if self.time_after_last_solution_update > self.time_after_last_state_update:
            elapsed_time = time() - self.time_after_last_solution_update
        else:
            elapsed_time = time() - self.time_after_last_state_update
        total_elapsed_time = time() - self.start_time
        self.time_after_last_state_update = time()

        info(f"Finished {finished_steps} steps in {strftime("%H:%M:%S.%f"[:-3], gmtime(total_elapsed_time))}")

        remaining_steps = self.remaining_steps(state.wishes.values())
        total_steps_guess = finished_steps + remaining_steps
        time_per_step = elapsed_time / max(1, finished_steps)
        total_time_guess = remaining_steps * time_per_step
        progress_guess = (100*finished_steps) / max(1, total_steps_guess)

        debug(f"Estimated progress: {progress_guess:<1} ({finished_steps}/{total_steps_guess} steps).")
        debug(
            f"Estimated time: {strftime("%H:%M:%S", gmtime(total_time_guess))} " +
            f"({strftime("%H:%M:%S.%f"[:-3], gmtime(time_per_step))} time per step)"
        )

    def log_solution_update(
            self,
            best_solution: Solution,
            new_solution: Solution
        ):
        elapsed_time = time() - self.time_after_last_solution_update
        total_elapsed_time = time() - self.start_time
        self.time_after_last_solution_update = time()

        info(
            f"Found {new_solution.index} improvements in " +
            f"{strftime("%H:%M:%S.%f"[:-3], gmtime(total_elapsed_time))}"
        )

        time_per_solution = elapsed_time / max(1, new_solution.index)
        total_time_guess = time_per_solution*self.generated_solutions_count_max

        debug(f"At most, {self.generated_solutions_count_max} times the program searches for an improvement.")
        debug(f"Allocated {new_solution.score} seekers instead of {best_solution.score} seekers.")
        debug(
            f"Estimated time: {strftime("%H:%M:%S", gmtime(total_time_guess))} " +
            f"({strftime("%H:%M:%S.%f"[:-3], gmtime(time_per_solution))} time per step)"
        )

    def log_final_solution(self, solution: Solution):
        info(f"{22*"-"} Finished Allocation {solution.name} {22*"-"}")

        total_elapsed_time = time() - self.start_time
        seekers_count = len(solution.parameters.seekers)
        events_count = len(solution.parameters.events)

        average_wishes = solution.total_wishes_count / max(1, seekers_count)
        unchecked_wishes = solution.unchecked_wishes_count
        checked_wishes = solution.total_wishes_count - unchecked_wishes
        average_checked_wishes = checked_wishes / max(1, seekers_count)

        allocated_seekers_count = len(solution.participations)
        allocated_seekers_count_percentage = (100*allocated_seekers_count) / max(1, seekers_count)

        debug(
            f"In {strftime("%H:%M:%S.%f"[:-3], gmtime(total_elapsed_time))} " +
            f"{solution.index} solutions were created."
        )
        debug(
            f"The best solution allocated {allocated_seekers_count}/{seekers_count} seekers " +
            f"(~{allocated_seekers_count_percentage}%) to " +
            f"{solution.capacity_sum} slots in {events_count} events."
        )
        debug(
            f"{checked_wishes} of {solution.total_wishes_count} wishes got checked " +
            f"(~{average_checked_wishes}/{average_wishes} per seeker)."
        )
