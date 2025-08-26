from typing import Literal, cast

ReaderStatsRadioActivitiy = Literal['active', 'inactive']

READER_STATS_RADIO_ACTIVITIY_VALUES: set[ReaderStatsRadioActivitiy] = { 'active', 'inactive',  }

def check_reader_stats_radio_activitiy(value: str) -> ReaderStatsRadioActivitiy:
    if value in READER_STATS_RADIO_ACTIVITIY_VALUES:
        return cast(ReaderStatsRadioActivitiy, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_RADIO_ACTIVITIY_VALUES!r}")
