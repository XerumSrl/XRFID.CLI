from typing import Literal, cast

QueryTarget = Literal['A', 'AB', 'B']

QUERY_TARGET_VALUES: set[QueryTarget] = { 'A', 'AB', 'B',  }

def check_query_target(value: str) -> QueryTarget:
    if value in QUERY_TARGET_VALUES:
        return cast(QueryTarget, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUERY_TARGET_VALUES!r}")
