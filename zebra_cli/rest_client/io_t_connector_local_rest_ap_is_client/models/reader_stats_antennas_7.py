from typing import Literal, cast

ReaderStatsAntennas7 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_7_VALUES: set[ReaderStatsAntennas7] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_7(value: str) -> ReaderStatsAntennas7:
    if value in READER_STATS_ANTENNAS_7_VALUES:
        return cast(ReaderStatsAntennas7, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_7_VALUES!r}")
