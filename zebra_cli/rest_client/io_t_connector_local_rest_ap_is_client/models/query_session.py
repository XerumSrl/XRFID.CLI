from typing import Literal, cast

QuerySession = Literal['S0', 'S1', 'S2', 'S3']

QUERY_SESSION_VALUES: set[QuerySession] = { 'S0', 'S1', 'S2', 'S3',  }

def check_query_session(value: str) -> QuerySession:
    if value in QUERY_SESSION_VALUES:
        return cast(QuerySession, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {QUERY_SESSION_VALUES!r}")
