from typing import Literal, cast

ReaderStatsPowerNegotiation = Literal['DISABLED', 'FAILURE', 'IN_PROGRESS', 'NOT_APPLICABLE', 'SUCCESS']

READER_STATS_POWER_NEGOTIATION_VALUES: set[ReaderStatsPowerNegotiation] = { 'DISABLED', 'FAILURE', 'IN_PROGRESS', 'NOT_APPLICABLE', 'SUCCESS',  }

def check_reader_stats_power_negotiation(value: str) -> ReaderStatsPowerNegotiation:
    if value in READER_STATS_POWER_NEGOTIATION_VALUES:
        return cast(ReaderStatsPowerNegotiation, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_POWER_NEGOTIATION_VALUES!r}")
