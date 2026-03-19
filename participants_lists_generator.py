from collections import defaultdict
from collections.abc import Generator

from data import Data, JuLei, Schulung

type Step = tuple[dict[Schulung, list[JuLei]], Schulung | None, JuLei | None]

def get_participants_lists(data: Data) -> dict[Schulung, list[JuLei]]:
    participants: dict[Schulung, list[JuLei]] = {s: list() for s in data.schulungen}
    for step in get_steps_of_getting_participants_lists(data):
        participants = step[0]
    return participants

# todo: Clean and fit everywhere else!!
asdöflj

def get_steps_of_getting_participants_lists(data: Data
        ) -> Generator[tuple[dict[Schulung, list[JuLei]], dict[Schulung, list[JuLei]]]]:
    participants: dict[Schulung, list[JuLei]] = defaultdict(list)
    wishes = data.get_wishes_of_juleis()
    unallocated_juleis = data.juleis[:]
    while len(unallocated_juleis) > 0:
        while len(unallocated_juleis) > 0:
            unallocated_julei = unallocated_juleis.pop()
            desired_schulung = wishes[unallocated_julei].pop()
            participants[desired_schulung].append(unallocated_julei)
        participants_copy = participants.copy()
        for schulung in participants.keys():
            if len(participants[schulung]) > schulung.capacity:
                participants[schulung].sort(key=lambda j:(
                    j.from_bw,
                    data.scores[desired_schulung][j]
                ))
                unallocated_juleis += participants[schulung][schulung.capacity:]
                participants[schulung] = participants[schulung][:schulung.capacity]
        yield participants_copy, participants
