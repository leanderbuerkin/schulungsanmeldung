# Schlungsanmeldung

This repository provides Python code to assign seekers (humans) to events.
This can be described as 
["finding a matching of a bipartite graph"](https://en.wikipedia.org/wiki/Bipartite_graph#Matching)

The goal is, to use it to assign "JuLeis" (seekers) to  "Schulung" (events).

## Usage

All commands are only tried on Linux Mint.
So feel free to contribute the commands for other operating systems.

### Optional: Create a Virtual Python Environment

```bash
python3 -m venv .venv 
```

### Install All Needed Packages

Remove the part before the `&` if you don't use a virtual python environment.

```bash
source .venv/bin/activate & pip install -r requirements.txt
```

## Explanation

There are multiple branches with feasible solutions.
Check first the `.odp`-file for a general overview.
The same content is also described here and in german in the other `.md`-file.

### The Problem

The JDAV BaWü organizes between 50 and 100 Schulungen per year.
Each Schulung has around 12 slots.
Roughly 700 JuLeis must be distributed to these slots.

### Key Assumptions

- Each JuLeis gets at most one slot (in this first distribution process)
- Since the Schulungen are very different, the JuLeis preferences must get collected and taken into consideration.
- JuLeis from Baden-Württemberg take always precedence over JuLeis from elsewhere
- The system should be fair.
- JuLeis that provide more information should not be punished for that.
- Only really necessary constraints should be implemented.
- A JuLei should only get no slot, if there is no slot free in any of the JuLeis wishes. 

### Input

The JuLeis get 2, 3 or more categories to which they can add as many Schulungen as they want.
German names could be "Lieblingsschulungen", "bevorzugte Schulungen" und "Notlösungen".

Providing less categories allows the program to give more JuLeis a slot.
Providing more categories allows the JuLei to communicate their preferences better.

The names and the amount can and should be changed over time.
E.g. if noone uses the category in the middle, maybe rename it or remove it.

For processing, the categories are treated separately:

- 1. cohort: "Lieblingsschulungen" from JuLeis from Baden-Württemberg
- 2. cohort: "bevorzugte Schulungen" from JuLeis from Baden-Württemberg
- 3. cohort: "Notlösungen" from JuLeis from Baden-Württemberg

- 4. cohort: "Lieblingsschulungen" from JuLeis not from Baden-Württemberg
- 5. cohort: "bevorzugte Schulugnen" from JuLeis not from Baden-Württemberg
- 6. cohort: "Notlösungen" from JuLeis not from Baden-Württemberg

This way it does not matter what the JuLeis choose (or not choose) in other categories and
are therefore not punished for providing more information.
Since all Schulungen in one category are considered equally liked/disliked by the JuLei,
it is not considered as "punishment" if one of them is chosen over another.

### Solutions

#### Random per Cohort: Robust, Simpler and Quotas can be added

For each cohort:

For each event we add all JuLeis to the remaining slots.
If there are more JuLeis then slots,
we randomly and/or by quota choose those that get a slot.

The event with the least interested JuLeis should always be handled next
so that as many JuLeis as possible get a slot.

#### Total Random: Robust, Simpler, Fairer and stronger Quotas can be added

Before processing, each event sorts the JuLeis
randomly and afterwards moves the JuLeis from Baden-Württemberg to the front
while preserving the random order.

Then for each JuLei, the wishes are sorted by the capacity of the Schulung,
(the total amount of wishes per Schulung) and randomly.

Afterwards all JuLeis are added to their first wish
and starting from the lowest ranking,
the surplus of JuLeis are reallocated to their next wishes.

#### Bipartite Matching: Complexer, gives as many JuLeis as possible a slot and weak Quotas can be added as tie-breaker

For each cohort,
[scipy.maximum_flow](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.maximum_flow.html)
finds the solution that gives as many JuLeis as possible a slot.

[scipy.maximum_flow](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.maximum_flow.html)
is used instead of
[maximum_bipartite_matching](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.maximum_bipartite_matching.html#scipy.sparse.csgraph.maximum_bipartite_matching)
because it the edges to the sink get the capacity of the Schulungen
and the matrizes are easier to create and understand.

After the best solution is found, for each event
we could check if kicking one JuLei and accepting a rejected one improves the quotas.
This should start with the event with the worst quota.
(This is not yet implemented)

All events should be checked multiple times,
since the newly kicked JuLeis might be able to improve the quotas.
This can probably loop (?) so it should just be done x times (depending on how long it takes).

Since always only one JuLeis is kicked while another one is added,
the new solution is also always an optimal solution.

## Contribute

### Save All Needed Packages

```bash
pip freeze > requirements.txt
```

### Programming Philosophie

Since this program is probably touched by volunteers,
it should be as robust and readable as possible.

The problem is best described functional.

While functional principles (like immutable attributes, properties and states)
are hard to enforce in Python, dataclasses help at least a bit.

In this case, creating new instances instead of mutating old ones
make the code easier to understand and
prevents errors like mistaking a copy for a reference.

### Notes

Storing and coloring Matrizes as `.xlsx` is faster and easier than using images.
