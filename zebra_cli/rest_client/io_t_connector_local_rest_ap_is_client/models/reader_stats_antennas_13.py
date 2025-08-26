from typing import Literal, cast

ReaderStatsAntennas13 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_13_VALUES: set[ReaderStatsAntennas13] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_13(value: str) -> ReaderStatsAntennas13:
    if value in READER_STATS_ANTENNAS_13_VALUES:
        return cast(ReaderStatsAntennas13, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_13_VALUES!r}")
