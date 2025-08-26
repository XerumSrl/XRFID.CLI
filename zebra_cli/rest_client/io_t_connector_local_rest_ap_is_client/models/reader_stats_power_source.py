from typing import Literal, cast

ReaderStatsPowerSource = Literal['DC', 'POE', 'POE+']

READER_STATS_POWER_SOURCE_VALUES: set[ReaderStatsPowerSource] = { 'DC', 'POE', 'POE+',  }

def check_reader_stats_power_source(value: str) -> ReaderStatsPowerSource:
    if value in READER_STATS_POWER_SOURCE_VALUES:
        return cast(ReaderStatsPowerSource, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_POWER_SOURCE_VALUES!r}")
