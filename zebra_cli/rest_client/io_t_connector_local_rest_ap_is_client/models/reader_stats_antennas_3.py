from typing import Literal, cast

ReaderStatsAntennas3 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_3_VALUES: set[ReaderStatsAntennas3] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_3(value: str) -> ReaderStatsAntennas3:
    if value in READER_STATS_ANTENNAS_3_VALUES:
        return cast(ReaderStatsAntennas3, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_3_VALUES!r}")
