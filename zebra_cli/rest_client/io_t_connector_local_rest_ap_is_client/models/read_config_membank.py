from typing import Literal, cast

ReadConfigMembank = Literal['EPC', 'RESERVED', 'TID', 'USER']

READ_CONFIG_MEMBANK_VALUES: set[ReadConfigMembank] = { 'EPC', 'RESERVED', 'TID', 'USER',  }

def check_read_config_membank(value: str) -> ReadConfigMembank:
    if value in READ_CONFIG_MEMBANK_VALUES:
        return cast(ReadConfigMembank, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READ_CONFIG_MEMBANK_VALUES!r}")
