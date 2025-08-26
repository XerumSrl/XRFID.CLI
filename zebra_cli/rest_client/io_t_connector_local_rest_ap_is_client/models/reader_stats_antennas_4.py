from typing import Literal, cast

ReaderStatsAntennas4 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_4_VALUES: set[ReaderStatsAntennas4] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_4(value: str) -> ReaderStatsAntennas4:
    if value in READER_STATS_ANTENNAS_4_VALUES:
        return cast(ReaderStatsAntennas4, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_4_VALUES!r}")
