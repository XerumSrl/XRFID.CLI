from typing import Literal, cast

WriteConfigMembank = Literal['EPC', 'RESERVED', 'TID', 'USER']

WRITE_CONFIG_MEMBANK_VALUES: set[WriteConfigMembank] = { 'EPC', 'RESERVED', 'TID', 'USER',  }

def check_write_config_membank(value: str) -> WriteConfigMembank:
    if value in WRITE_CONFIG_MEMBANK_VALUES:
        return cast(WriteConfigMembank, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {WRITE_CONFIG_MEMBANK_VALUES!r}")
