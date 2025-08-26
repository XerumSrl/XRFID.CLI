from typing import Literal, cast

ReaderStatsAntennas6 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_6_VALUES: set[ReaderStatsAntennas6] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_6(value: str) -> ReaderStatsAntennas6:
    if value in READER_STATS_ANTENNAS_6_VALUES:
        return cast(ReaderStatsAntennas6, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_6_VALUES!r}")
