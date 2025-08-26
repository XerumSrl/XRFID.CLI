from typing import Literal, cast

ReaderStatsAntennas8 = Literal['connected', 'disconnected']

READER_STATS_ANTENNAS_8_VALUES: set[ReaderStatsAntennas8] = { 'connected', 'disconnected',  }

def check_reader_stats_antennas_8(value: str) -> ReaderStatsAntennas8:
    if value in READER_STATS_ANTENNAS_8_VALUES:
        return cast(ReaderStatsAntennas8, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_ANTENNAS_8_VALUES!r}")
