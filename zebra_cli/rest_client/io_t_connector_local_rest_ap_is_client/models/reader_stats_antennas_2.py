from typing import Literal, cast

ReaderStatsAntennas2 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_2_VALUES: set[ReaderStatsAntennas2] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_2(value: str) -> ReaderStatsAntennas2:
    if value in READER_STATS_ANTENNAS_2_VALUES:
        return cast(ReaderStatsAntennas2, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_2_VALUES!r}")
