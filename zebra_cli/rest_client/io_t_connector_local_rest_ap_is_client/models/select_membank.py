from typing import Literal, cast

SelectMembank = Literal['EPC', 'RES', 'TID', 'USER']

SELECT_MEMBANK_VALUES: set[SelectMembank] = { 'EPC', 'RES', 'TID', 'USER',  }

def check_select_membank(value: str) -> SelectMembank:
    if value in SELECT_MEMBANK_VALUES:
        return cast(SelectMembank, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {SELECT_MEMBANK_VALUES!r}")
