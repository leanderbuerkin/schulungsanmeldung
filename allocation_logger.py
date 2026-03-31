from collections.abc import Iterable
from logging import DEBUG, INFO, basicConfig, debug, info
from pathlib import Path
from time import gmtime, strftime, time

from allocator import Allocator
from data_structures import Event, Parameters, Solution

class Logger:
    allocator: Allocator
    previous_solution: Solution | None
    start_time: float
    last_time: float
    updates_count: int

    @property
    def seekers_count(self) -> int:
        return len(self.allocator.parameters.seekers)
    @property
    def events_count(self) -> int:
        return len(self.allocator.parameters.events)
    @property
    def capacity_sum(self) -> int:
        return sum(event.capacity for event in self.allocator.parameters.events)
    @property
    def priorities_count(self) -> int:
        prioritizations = self.allocator.parameters.get_flattened_prioritizations()
        return sum(len(prioritization) for prioritization in prioritizations.values())
    @property
    def average_priorities_count(self) -> float:
        return self.priorities_count / self.seekers_count
    @property
    def runtime(self) -> float:
        return time() - self.start_time
    @property
    def runtime_since_last_update(self) -> float:
        return time() - self.last_time
    @property
    def time_per_update(self) -> float:
        return self.runtime / max(1, self.updates_count)

    @property
    def remaining_updates_count_guess(self) -> int:
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
        return max(len(prioritization) for prioritization in self.allocator.prioritizations.values())
    @property
    def total_updates_count_guess(self) -> int:
        return self.updates_count + self.remaining_updates_count_guess
    @property
    def total_runtime_guess(self) -> float:
        return self.remaining_updates_count_guess * self.time_per_update
    @property
    def progress_guess(self) -> float:
        return (100*self.updates_count) / max(1, self.total_updates_count_guess)

    def __init__(self, allocator: Allocator, previous_solution: Solution | None, verbose: bool = True):
        self.allocator = allocator
        self.previous_solution = previous_solution
        self.start_time = time()
        self.last_time = time()
        self.updates_count = 0
        self.__init_logger(verbose)
        self.log_start()

    def __init_logger(self, verbose: bool = True):
        log_file_path = Path(f"{self.allocator.name}.log")
        with open(log_file_path, "w") as potentially_filled_file:
            potentially_filled_file.write("")

        basicConfig(
            level=DEBUG if verbose else INFO,
            format="%(asctime)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S.%f",
            filename=log_file_path
        )
    
    def log_start(self):
        info(f"{22*"-"} Started Allocation {self.allocator.name} {22*"-"}")
        debug(
            f"{self.seekers_count} seekers that provide " +
            f"{self.average_priorities_count:.1f} events as priorities " +
            f"need to be allocated to {self.events_count} events " +
            f"with a total of {self.capacity_sum} slots."
        )

    def log_update(self):
        info(f"Finished {self.updates_count} steps in {self._as_str(self.runtime)}")
        debug(
            f"Estimated progress: {self.progress_guess:<1} " +
            f"({self.updates_count}/{self.total_updates_count_guess} steps)."
        )
        debug(
            f"Estimated time: {self._as_str(self.total_runtime_guess)} " +
            f"{self._as_str(self.time_per_update)} time per step)"
        )
        self.last_time = time()

    @staticmethod
    def _as_str(time_in_seconds: float) -> str:
        return strftime("%H:%M:%S.%f", gmtime(time_in_seconds))












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
