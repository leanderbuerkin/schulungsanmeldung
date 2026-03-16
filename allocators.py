"""
Core problem:
The goal, to provide as many JuLeis a place as possible
can not be reached without incentivicing all JuLeis to only provide one preference/wish.

If we allocate a JuLei to the second wish, because there is space
and all other JuLeis in the first wish do not have an alternative,
we treat the JuLeis that provide less alternatives better.

So the only valid option can be:
- Assign JuLeis to their highest priority without regards to its capacity
- Remove as many JuLeis randomly from each Schulung that has to many JuLeis
- Assign all removed JuLeis to their second priority
- Again remove as many JuLeis randomly from each Schulung that has to many JuLeis

It is debatable whether to choose randomly out of all JuLeis or only the newly assigned at the second removall-process.

In principle, the goal is, that every Schulung chooses transparently and fairly from all JuLeis.
So we start by giving each Schulung a shuffled list of JuLeis.
The Schulung tries to gather as many JuLeis as far left as possible.

So we can give each Schulung a JuLei and if it is preferred,
we get back another one. If there is space, we don't get anything
"""
from pathlib import Path

from data_containers import Problem
from file_saver import save_to_xlsx

def allocate(p: Problem, xlsx_file_path: Path) -> Problem:
    for julei_index, julei in enumerate(p.juleis):
        while julei is not None and len(julei.wishes) > 0:
            best_schulung_index = julei.wishes.pop(0)
            julei = p.schulungen[best_schulung_index].update_participants(julei)
            save_to_xlsx(p, xlsx_file_path, f"julei_{julei_index:03d}")
    return p
