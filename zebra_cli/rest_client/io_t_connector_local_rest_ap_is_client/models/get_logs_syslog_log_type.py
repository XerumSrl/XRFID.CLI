from typing import Literal, cast

GetLogsSyslogLogType = Literal['radioPacketLog', 'RcErrorLog', 'RcInfoLog', 'RcWarningLog', 'RgErrorLog', 'RgWarningLog', 'syslog']

GET_LOGS_SYSLOG_LOG_TYPE_VALUES: set[GetLogsSyslogLogType] = { 'radioPacketLog', 'RcErrorLog', 'RcInfoLog', 'RcWarningLog', 'RgErrorLog', 'RgWarningLog', 'syslog',  }

def check_get_logs_syslog_log_type(value: str) -> GetLogsSyslogLogType:
    if value in GET_LOGS_SYSLOG_LOG_TYPE_VALUES:
        return cast(GetLogsSyslogLogType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {GET_LOGS_SYSLOG_LOG_TYPE_VALUES!r}")
