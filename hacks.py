from collections.abc import Generator
from dataclasses import dataclass, fields
# from inspect import getmembers
from types import MappingProxyType
from typing import Any, TypeVar

KEY_TYPE = TypeVar("KEY_TYPE")
VALUE_TYPE = TypeVar("VALUE_TYPE")
type FrozenDict[K, VALUE_TYPE] = MappingProxyType[K, VALUE_TYPE]
def freeze_dict(any_dict: dict[KEY_TYPE, VALUE_TYPE]) -> FrozenDict[KEY_TYPE, VALUE_TYPE]:
    return MappingProxyType(any_dict)

@dataclass(frozen=True, slots=True, kw_only=True)
class Unpackable:
    """
    Allows to unpack dataclasses with **instance.
    In comparison to dataclasses.asdict() this does not unpack nested dataclasses.
    """
    def keys(self) -> Generator[str]:
        yield from (f.name for f in fields(self))
        # Unpacks the @properties as if they were normal fields.
        # yield from (name for name, _  in getmembers(self, lambda m: isinstance(m, property)))

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)
