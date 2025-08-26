from typing import Literal, cast

DelLogsSyslogLogType = Literal['radioPacketLog', 'RcErrorLog', 'RcInfoLog', 'RcWarningLog', 'RgErrorLog', 'RgWarningLog', 'syslog']

DEL_LOGS_SYSLOG_LOG_TYPE_VALUES: set[DelLogsSyslogLogType] = { 'radioPacketLog', 'RcErrorLog', 'RcInfoLog', 'RcWarningLog', 'RgErrorLog', 'RgWarningLog', 'syslog',  }

def check_del_logs_syslog_log_type(value: str) -> DelLogsSyslogLogType:
    if value in DEL_LOGS_SYSLOG_LOG_TYPE_VALUES:
        return cast(DelLogsSyslogLogType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DEL_LOGS_SYSLOG_LOG_TYPE_VALUES!r}")
