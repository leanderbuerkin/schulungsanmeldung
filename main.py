
# todo: Add tests (is really everything unchanged after writing and reading xlsx)

from os import makedirs
from pathlib import Path

from allocator import find_best_allocation
from generators import generate_random_input_data
from xlsx import XLSX, XLSXPlotter, XLSXWriter



DATA_DIRECTORY = Path("data")

input_data = generate_random_input_data(40, 200, 50, 3, 5, 4, 0, 3)

solution = find_best_allocation(input_data)

xlsx = XLSX.get_new_workbook(solution.name)
XLSXWriter.add_data_to_xlsx(input_data, xlsx)
XLSXWriter.add_log_file_to_xlsx(input_data.log_file_path, xlsx)
XLSXPlotter.add_plot_to_xlsx(xlsx, solution)

makedirs(DATA_DIRECTORY, exist_ok=True)
xlsx.save(DATA_DIRECTORY/f"{solution.name}.xlsx")
input_data = generate_random_input_data(20, 300, 80, 8, 12, 0, 50)








"""

    # @property
    # def capacity_sum(self) -> int:
    #     return sum(event.capacity for event in self.events)
    # @property
    # def wishes_count(self) -> int:
    #     return sum(len(wishes) for wishes in self.prioritizations.values())
    @property
    def unallocatable_seekers(self) -> tuple[Seeker, ...]:
        return tuple(seeker for seeker, wishes in self.wishes.items() if len(wishes) == 0)
    @property
    def allocations(self) -> FrozenDict[Seeker, Event]:
        return freeze_dict({seeker: wishes[0] for seeker, wishes in self.wishes.items() if len(wishes) > 0})
    @property
    def overcrowded_events(self) -> FrozenDict[Event, tuple[Seeker, ...]]:
        overcrowded_events: dict[Event, tuple[Seeker, ...]] = defaultdict(tuple)

        for event, candidates in self.candidates.items():
            if len(candidates) > event.capacity:
                overcrowded_events[event] = candidates

        return freeze_dict(overcrowded_events)



    @property
    def unsatisfied_demand(self) -> FrozenDict[Event, int]:
        wishes_counts: dict[Event, int] = defaultdict(int)

        for seeker in self.unallocatable_seekers:
            for event in seeker.flattened_wishes:
                wishes_counts[event] += 1

        return freeze_dict(wishes_counts)

    @property
    def total_wishes(self) -> FrozenDict[Seeker, tuple[Event, ...]]:
        return self.initial_state.wishes
    @property
    def accepted_wishes(self) -> FrozenDict[Seeker, tuple[Event]]:
        return freeze_dict({s: (e,) for s, e in self.final_state.allocations.items()})
    @property
    def unchecked_wishes(self) -> FrozenDict[Seeker, tuple[Event, ...]]:
        return freeze_dict({s: tuple(es[1:]) for s, es in self.final_state.wishes.items()})

    @property
    def total_wishes_count(self) -> int:
        return self.parameters.wishes_count
    @property
    def unchecked_wishes_count(self) -> int:
        return sum(len(wishes) for wishes in self.unchecked_wishes.values())
    @property
    def capacity_sum(self) -> int:
        return self.parameters.capacity_sum

"""