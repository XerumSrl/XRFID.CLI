from typing import Literal, cast

ReaderStatsNtpType1 = Literal['NOT_CONFIGURED']

READER_STATS_NTP_TYPE_1_VALUES: set[ReaderStatsNtpType1] = { 'NOT_CONFIGURED',  }

def check_reader_stats_ntp_type_1(value: str) -> ReaderStatsNtpType1:
    if value in READER_STATS_NTP_TYPE_1_VALUES:
        return cast(ReaderStatsNtpType1, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {READER_STATS_NTP_TYPE_1_VALUES!r}")
