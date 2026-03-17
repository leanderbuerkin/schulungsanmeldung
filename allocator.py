"""
In a fair solution, each JuLei has the same chance to get into a Schulung
if there are no contradicting rules.

So if multiple JuLeis apply for a Schulung, we must select randomly.
We achieve this by giving each Schulung one unique score for each JuLei.
If we need to decide which JuLeis we added, we choose those with the highest scores.

This is fair, because the scores are random and each JuLei has the same chances for a good score.

In praxis, we add each JuLei to her/his favorite Schulung one by one.
When we surpass the capacity of a Schulung, we decide which JuLei gets kicked out.
Maybe we even kick out the JuLei we just added - maybe another one.

Then we add the kicked out JuLei to her/his second favorite Schulung.
If this also pushes this Schulung above its capacity,
we decide again, which JuLei gets kicked out of this Schulung.

Such a chain can last till a JuLei finds a free slot or
does not want to participate in any other Schulung.
Either way, the chain can not run indefinitely.
"""

from data_containers import JuLei, Problem, Schulung
from file_saver import save_to_xlsx
from time import time

def _pop_least_fitting_julei(p: Problem, schulung: Schulung) -> JuLei:
    juleis = [p.juleis[j_id] for j_id in p.participants[schulung.id]]
    if any((not j.from_bw for j in juleis)):
        juleis = [j for j in juleis if not j.from_bw]
    least_fitting_julei = min(juleis, key=lambda j: schulung.scores[j.id])
    p.participants[schulung.id].remove(least_fitting_julei.id)
    return least_fitting_julei

def _update_participants(p: Problem, schulung: Schulung, julei: JuLei) -> JuLei | None:
    p.participants[schulung.id].append(julei.id)
    if len(p.participants[schulung.id]) > schulung.capacity:
        return _pop_least_fitting_julei(p, schulung)

def allocate(p: Problem):
    start_time = time()
    for finished_juleis, julei in enumerate(p.juleis.values()):
        while julei is not None and len(p.remaining_wishes[julei.id]) > 0:
            best_schulung = p.schulungen[p.remaining_wishes[julei.id].pop(0)]
            julei = _update_participants(p, best_schulung, julei)
            if len(p.schulungen)*len(p.juleis) < 1000:
                save_to_xlsx(p, f"{time()-start_time:.2f} s")
        print(f"{finished_juleis} of {len(p.juleis)} JuLeis assigned")
    save_to_xlsx(p, f"{time()-start_time:.2f} s")
