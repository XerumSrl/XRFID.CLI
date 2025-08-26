from typing import Literal, cast

LogLevelComponentsItemLevel = Literal['DEBUG', 'ERROR', 'FATAL', 'INFO', 'OFF', 'WARNING']

LOG_LEVEL_COMPONENTS_ITEM_LEVEL_VALUES: set[LogLevelComponentsItemLevel] = { 'DEBUG', 'ERROR', 'FATAL', 'INFO', 'OFF', 'WARNING',  }

def check_log_level_components_item_level(value: str) -> LogLevelComponentsItemLevel:
    if value in LOG_LEVEL_COMPONENTS_ITEM_LEVEL_VALUES:
        return cast(LogLevelComponentsItemLevel, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {LOG_LEVEL_COMPONENTS_ITEM_LEVEL_VALUES!r}")
