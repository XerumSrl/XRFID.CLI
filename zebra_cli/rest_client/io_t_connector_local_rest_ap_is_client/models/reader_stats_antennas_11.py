from typing import Literal, cast

ReaderStatsAntennas11 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_11_VALUES: set[ReaderStatsAntennas11] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_11(value: str) -> ReaderStatsAntennas11:
    if value in READER_STATS_ANTENNAS_11_VALUES:
        return cast(ReaderStatsAntennas11, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_11_VALUES!r}")
