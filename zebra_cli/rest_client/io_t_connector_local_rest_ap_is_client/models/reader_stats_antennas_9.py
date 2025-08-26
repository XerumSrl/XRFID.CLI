from typing import Literal, cast

ReaderStatsAntennas9 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_9_VALUES: set[ReaderStatsAntennas9] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_9(value: str) -> ReaderStatsAntennas9:
    if value in READER_STATS_ANTENNAS_9_VALUES:
        return cast(ReaderStatsAntennas9, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_9_VALUES!r}")
