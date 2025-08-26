from typing import Literal, cast

QuerySel = Literal['ALL', 'NOT_SL', 'SL']

QUERY_SEL_VALUES: set[QuerySel] = { 'ALL', 'NOT_SL', 'SL',  }

def check_query_sel(value: str) -> QuerySel:
    if value in QUERY_SEL_VALUES:
        return cast(QuerySel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUERY_SEL_VALUES!r}")
