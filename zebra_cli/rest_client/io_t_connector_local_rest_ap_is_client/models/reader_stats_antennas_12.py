from typing import Literal, cast

ReaderStatsAntennas12 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_12_VALUES: set[ReaderStatsAntennas12] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_12(value: str) -> ReaderStatsAntennas12:
    if value in READER_STATS_ANTENNAS_12_VALUES:
        return cast(ReaderStatsAntennas12, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_12_VALUES!r}")
