from types import MappingProxyType
from typing import TypeVar

KEY_TYPE = TypeVar("KEY_TYPE")
VALUE_TYPE = TypeVar("VALUE_TYPE")
type FrozenDict[K, VALUE_TYPE] = MappingProxyType[K, VALUE_TYPE]
def freeze_dict(any_dict: dict[KEY_TYPE, VALUE_TYPE]) -> FrozenDict[KEY_TYPE, VALUE_TYPE]:
    return MappingProxyType(any_dict)
