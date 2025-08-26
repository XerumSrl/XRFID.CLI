from typing import Literal, cast

ReaderStatsRadioConnection = Literal['connected', 'disconnected']

READER_STATS_RADIO_CONNECTION_VALUES: set[ReaderStatsRadioConnection] = { 'connected', 'disconnected',  }

def check_reader_stats_radio_connection(value: str) -> ReaderStatsRadioConnection:
    if value in READER_STATS_RADIO_CONNECTION_VALUES:
        return cast(ReaderStatsRadioConnection, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_RADIO_CONNECTION_VALUES!r}")
