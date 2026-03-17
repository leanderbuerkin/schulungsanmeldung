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

from collections.abc import Generator

from data_containers import JuLei, Problem, Schulung

def _pop_least_fitting_julei(p: Problem, schulung: Schulung) -> JuLei:
    p.participants[schulung] = sorted(p.participants[schulung], key=lambda j: p.scores[schulung][j])
    least_fitting_julei = p.participants[schulung][0]
    for julei in p.participants[schulung]:
        if not p.from_bw[julei]:
            least_fitting_julei = julei
    p.participants[schulung].remove(least_fitting_julei)
    return least_fitting_julei

def _update_participants(p: Problem, schulung: Schulung, julei: JuLei) -> JuLei | None:
    p.participants[schulung].append(julei)
    if len(p.participants[schulung]) > schulung.capacity:
        return _pop_least_fitting_julei(p, schulung)

def allocate(p: Problem) -> Generator[JuLei]:
    for julei in p.remaining_wishes.keys():
        if not(p.get_allocation(julei) is None):
            continue
        while not(julei is None) and len(p.remaining_wishes[julei]) > 0:
            yield julei
            best_schulung = p.remaining_wishes[julei].pop(0)
            julei = _update_participants(p, best_schulung, julei)
