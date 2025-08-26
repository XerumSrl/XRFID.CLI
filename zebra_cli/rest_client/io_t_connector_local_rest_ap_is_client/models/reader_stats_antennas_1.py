from typing import Literal, cast

ReaderStatsAntennas1 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_1_VALUES: set[ReaderStatsAntennas1] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_1(value: str) -> ReaderStatsAntennas1:
    if value in READER_STATS_ANTENNAS_1_VALUES:
        return cast(ReaderStatsAntennas1, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_1_VALUES!r}")
