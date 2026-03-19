"""
These dataclasses are used as keys in dicts.

That's why they are frozen, get a unique id and are using tuples.
"""

from dataclasses import dataclass

type UniqueJuLeiId = int    # just for readability
type UniqueSchulungsId = int    # just for readability

# They are used as keys in dictionaries:
# So
@dataclass(frozen=True)
class JuLei:
    id: UniqueJuLeiId
    from_bw: bool
    wishes: tuple[UniqueSchulungsId, ...]

# They are frozen and get a unique id because they are used as keys in dictionaries.
@dataclass(frozen=True)
class Schulung:
    id: UniqueSchulungsId
    capacity: int
