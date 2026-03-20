from collections.abc import Generator
from dataclasses import dataclass, fields
from inspect import getmembers
from typing import Any

@dataclass(frozen=True, slots=True, kw_only=True)
class Unpackable:
    """
    Allows to unpack dataclasses with **instance.


    Using asdict() on dataclass instances
    
    - does not return properties (which is only needed in this context)
    - converts dataclass instances inside as well
    """
    def keys(self) -> Generator[str]:
        yield from (f.name for f in fields(self))
        yield from (name for name, _  in getmembers(self, lambda m: isinstance(m, property)))

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
