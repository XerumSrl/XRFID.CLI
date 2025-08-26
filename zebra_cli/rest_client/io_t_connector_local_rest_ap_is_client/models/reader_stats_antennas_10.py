from typing import Literal, cast

ReaderStatsAntennas10 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_10_VALUES: set[ReaderStatsAntennas10] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_10(value: str) -> ReaderStatsAntennas10:
    if value in READER_STATS_ANTENNAS_10_VALUES:
        return cast(ReaderStatsAntennas10, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_10_VALUES!r}")
