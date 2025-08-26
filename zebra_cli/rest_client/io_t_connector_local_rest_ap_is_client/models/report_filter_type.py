from typing import Literal, cast

ReportFilterType = Literal['PER_ANTENNA', 'RADIO_WIDE']

REPORT_FILTER_TYPE_VALUES: set[ReportFilterType] = { 'PER_ANTENNA', 'RADIO_WIDE',  }

def check_report_filter_type(value: str) -> ReportFilterType:
    if value in REPORT_FILTER_TYPE_VALUES:
        return cast(ReportFilterType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {REPORT_FILTER_TYPE_VALUES!r}")
