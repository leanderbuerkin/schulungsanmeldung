from collections import defaultdict
from dataclasses import dataclass
import numpy as np
from scipy.sparse import csr_array
from scipy.sparse.csgraph import maximum_flow

@dataclass(frozen=True, slots=True, kw_only=True)
class Event:
    index: int # makes each instance unique
    capacity: int

@dataclass(frozen=True, slots=True, kw_only=True)
class Seeker:
    index: int # makes each instance unique
    from_baden_wuerttemberg: bool

def get_solution(
        ranked_wishes: dict[int, dict[Seeker, list[Event]]]
    ) -> dict[Event, list[Seeker]]:
    participants: dict[Event, list[Seeker]] = defaultdict(list)

    for allow_seekers_from_everywhere in [False, True]:
        for rank in sorted(ranked_wishes.keys()):
            wishes = ranked_wishes[rank]
            allocated_seekers = {s for seekers in participants.values() for s in seekers}
            events = [
                event for events in wishes.values() for event in events
                if event.capacity > len(participants[event])
            ]
            seekers = [
                seeker
                for seeker in wishes.keys()
                if ((allow_seekers_from_everywhere or seeker.from_baden_wuerttemberg)
                    and seeker not in allocated_seekers and len(wishes[seeker]) > 0)
            ]
            if len(seekers) == 0 or len(events) == 0:
                continue

            columns_count = len(["SOURCE"]) + len(seekers) + len(events) + len(["SINK"])
            rows_count = columns_count
            source_index = 0
            sink_index = columns_count - 1

            seeker_indizes = {
                seeker: seeker_index
                for seeker_index, seeker in enumerate(seekers, 1)
            }
            event_indizes = {
                event: event_index
                for event_index, event in enumerate(events, 1 + len(seekers))
            }

            adjacency_matrix = np.zeros((rows_count, columns_count), dtype=int)

            # Source to seekers: Capacity 1 cause each seeker can get at most one slot
            for seeker in seekers:
                adjacency_matrix[source_index, seeker_indizes[seeker]] = 1

            # Seekers to events: Capacity 1 cause each seeker can only get one slot of an event
            for seeker in seekers:
                for event in wishes[seeker]:
                    if event not in events:
                        continue  # the event is full or otherwise not choosable
                    adjacency_matrix[seeker_indizes[seeker], event_indizes[event]] = 1
            
            # Events to sink: Capacity varies depending on the free slots of the event
            for event in events:
                remaining_capacity = event.capacity - len(participants[event])
                if remaining_capacity > 0:
                    adjacency_matrix[event_indizes[event], sink_index] = remaining_capacity

            maximal_flow = maximum_flow(csr_array(adjacency_matrix), source_index, sink_index)
            matrix = maximal_flow.flow.toarray()

            for seeker in seekers:
                for event in wishes[seeker]:
                    if event not in events:
                        continue  # the event is full or otherwise not choosable
                    if matrix[seeker_indizes[seeker], event_indizes[event]] > 0:
                        participants[event].append(seeker)
                        break

    return participants
