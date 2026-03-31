from logging import DEBUG, INFO, basicConfig, debug, info
from pathlib import Path
from time import gmtime, strftime, time

from allocator import Allocator
from data_structures import Solution

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
        return self._in_percent(self.updates_count, self.total_updates_count_guess)

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

    def log_end(self, solution: Solution):

        info(f"{22*"-"} Finished Allocation {self.allocator.name} in {self._as_str(self.runtime)} {22*"-"}")
        debug(
            f"{self.seekers_count} seekers that provide " +
            f"{self.average_priorities_count:.1f} events as priorities " +
            f"got allocated to {self.events_count} events " +
            f"with a total of {self.capacity_sum} slots."
        )
        satisfaction = self._in_percent(solution.satisfied_seekers_count, self.seekers_count)
        debug(
            f"After {self.updates_count} updates, this new solution " +
            f"satisfies {solution.satisfied_seekers_count}" +
            f"/{self.seekers_count} seekers ({satisfaction:.1}%)."
        )
        if self.previous_solution:
            previous_satisfaction = self._in_percent(self.previous_solution.satisfied_seekers_count, self.seekers_count)
            debug(
                f"The previously best solution satisfied " +
                f"{self.previous_solution.satisfied_seekers_count}" +
                f"/{self.seekers_count} seekers ({previous_satisfaction:.1}%)."
            )

    @staticmethod
    def _as_str(time_in_seconds: float) -> str:
        return strftime("%H:%M:%S.%f", gmtime(time_in_seconds))

    @staticmethod
    def _in_percent(value: float, maximum: float) -> float:
        return (100*value) / max(1, maximum)
