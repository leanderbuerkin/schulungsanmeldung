# Schlungsanmeldung

This repository provides Python code to assign humans (by priorities and rules) to events.
It is used by the JDAV BaWü to determine the JuLeis per Schulung.

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

## Contribute

### Save All Needed Packages

```bash
pip freeze > requirements.txt
```

## Explanation

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

After randomly choosing the scores the rest of the program is unambiguous:
So it is enough to save the juleis, schulungen and the scores
to revisit each step and reach the same result.

## Notes

Storing and coloring Matrizes as `.xlsx` is faster and easier than using images.
