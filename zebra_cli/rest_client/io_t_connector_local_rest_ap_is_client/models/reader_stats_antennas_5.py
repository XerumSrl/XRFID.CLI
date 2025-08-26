from typing import Literal, cast

ReaderStatsAntennas5 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_5_VALUES: set[ReaderStatsAntennas5] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_5(value: str) -> ReaderStatsAntennas5:
    if value in READER_STATS_ANTENNAS_5_VALUES:
        return cast(ReaderStatsAntennas5, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_5_VALUES!r}")
