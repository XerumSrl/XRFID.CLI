from typing import Literal, cast

ReaderStatsAntennas0 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_0_VALUES: set[ReaderStatsAntennas0] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_0(value: str) -> ReaderStatsAntennas0:
    if value in READER_STATS_ANTENNAS_0_VALUES:
        return cast(ReaderStatsAntennas0, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_0_VALUES!r}")
